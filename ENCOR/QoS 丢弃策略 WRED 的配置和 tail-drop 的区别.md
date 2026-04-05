
# Tail-Drop 的问题

队列满了才开始丢包，而且同时丢弃所有 TCP 流的包。TCP 检测到丢包后触发拥塞控制，所有流同时把窗口缩小到最小值，带宽利用率骤降。等所有流同时慢启动恢复，带宽又同时飙升，队列再次打满，再次全部丢包——这就是 TCP 全局同步，带宽利用率在高低之间反复震荡。

```
带宽利用率

100% │▓▓▓▓▓     ▓▓▓▓▓     ▓▓▓▓▓
     │     ▓▓▓▓▓     ▓▓▓▓▓     ▓▓▓  ← Tail-Drop：锯齿波，全局同步
 50% │
     │─────────────────────────────▶ 时间

100% │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
     │                               ← WRED：平稳，各流独立调整
 50% │
```

# WRED 的解决思路

队列还没满时就开始随机丢包，不同 TCP 流在不同时间触发拥塞控制，窗口缩小的时间错开，带宽利用率保持平稳。

WRED 有三个门限控制丢弃概率：

```
丢弃概率

100% │                              ┌──────── tail-drop（全丢）
     │                         ╱───┘
     │                    ╱───╱
  0% │───────────────────╱
     │         │         │
               min       max        队列深度（平均）
               门限       门限
```

- 队列深度 < `min-threshold`：不丢包，正常转发

- 队列深度在 `min` 和 `max` 之间：按概率随机丢包，概率随深度线性增加

- 队列深度 > `max-threshold`：全部丢弃，等同 tail-drop

WRED 只对 TCP 有意义——UDP（语音、视频）丢了就丢了，不会触发拥塞控制，所以语音队列（LLQ priority）不用也不能加 WRED。

# 基础配置

最简单的写法，在 class 块里加一行：

```
policy-map WRED_DEMO
 class CRITICAL_DATA
  bandwidth percent 30
  random-detect                ← 默认 WRED，基于 IP Precedence 区分门限
```

推荐写法，基于 DSCP 区分丢弃概率：

```
policy-map WRED_DEMO
 class CRITICAL_DATA
  bandwidth percent 30
  random-detect dscp-based     ← 不同 DSCP 值有不同的 min/max 门限
```

`dscp-based` 的效果：AF31（DSCP 26）比 AF32（28）比 AF33（30）的 min 门限更高，意味着在同样的队列深度下，AF33 更容易被丢弃，AF31 更受保护。这正好配合 Policing 的降级策略——超速流量被标成 AF32/AF33，拥塞时优先被 WRED 丢弃。

# 手动调整门限（精细控制）

```
policy-map WRED_CUSTOM
 class CRITICAL_DATA
  bandwidth percent 30
  random-detect dscp-based

  random-detect dscp af31 28 40 10
  ← dscp值  min  max  mark-prob分母
  ← AF31：min=28包，max=40包，丢弃概率最大 1/10

  random-detect dscp af32 24 40 10
  ← AF32：min更低，更容易被丢弃

  random-detect dscp af33 20 40 10
  ← AF33：min最低，最容易被丢弃

  random-detect dscp default 16 40 10
  ← 没有 DSCP 标记的流量，最容易丢
```

`mark-prob` 是分母，`1/10` 表示当队列在 min 和 max 之间时，最大丢弃概率是 10%。值越小概率越高，越激进。

# 验证输出解读

```
R1#show policy-map interface e0/1
  Class-map: CRITICAL_DATA
    Queueing
    queue limit 64 packets
    (queue depth/total drops/no-buffer drops) 3/120/0
     ↑队列当前深度  ↑WRED丢的包  ↑队列满了丢的包

    exponential weight: 9       ← 平均队列深度的计算权重，越大越平滑
    mean queue depth: 18        ← 当前平均队列深度，在 min/max 之间说明 WRED 在工作

    dscp    min-th  max-th  mark-prob
    ------------------------------------------
    af31      28      40       1/10
    af32      24      40       1/10    ← 门限更低，更容易丢
    af33      20      40       1/10
    default   16      40       1/10    ← 无标记流量最先被丢
```

关键判断：`no-buffer drops` 应该接近 0。如果这个数字很大，说明队列经常打满，WRED 没来得及发挥作用，需要加大队列深度或增加 bandwidth percent。

`total drops` 有数是正常的，说明 WRED 在工作，随机丢包控制了队列深度，反而是好事。

# 和 tail-drop 的完整对比

|\|Tail-Drop|WRED|
|:--:|:--:|:--:|
|丢弃时机|队列满才丢|队列变深时概率丢|
|TCP 全局同步|有，带宽锯齿|无，各流独立调整|
|UDP 流量影响|直接丢|直接丢（一样）|
|DSCP 差异化|无|有（dscp-based）|
|配置复杂度|无需配置|一行或多行|
|适用场景|语音/视频队列|数据队列|

# 使用场景的判断原则

```
VOICE class（priority）
  → 不加 WRED，不加 random-detect
  → 语音包丢了就没了，不会重传，随机丢只会让通话质量更差
  → 靠 queue-limit 控制队列深度，超出直接 tail-drop

VIDEO class（bandwidth）
  → 可以加 WRED，但收益有限（视频也是 UDP）
  → 主要靠 bandwidth 保证不拥塞

DATA class（bandwidth）
  → 必须加 WRED + dscp-based
  → TCP 流量的标配，避免全局同步

class-default（fair-queue）
  → fair-queue 内置了类似 WRED 的机制，不需要再加 random-detect
```

最后一个细节：`random-detect` 和 `queue-limit` 可以同时写，WRED 在队列还没满时工作，`queue-limit` 是最后的硬上限保底。两者不冲突，配合使用。