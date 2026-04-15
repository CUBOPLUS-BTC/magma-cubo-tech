<script lang="ts">
  import { LineChart } from 'layerchart';
  import type { DayAnalysis } from '$lib/models/simulation';

  let { data }: { data: DayAnalysis[] } = $props();
</script>

<div class="h-80 w-full">
  <LineChart
    {data}
    x="wait_days"
    series={[
      {
        key: 'avg_return',
        value: 'avg_return',
        color: 'hsl(38, 92%, 50%)'
      },
      {
        key: 'best_case',
        value: 'best_case',
        color: 'hsl(142, 76%, 36%)',
        props: { strokeDasharray: '4 2' }
      },
      {
        key: 'worst_case',
        value: 'worst_case',
        color: 'hsl(0, 84%, 60%)',
        props: { strokeDasharray: '4 2' }
      }
    ]}
    props={{
      xAxis: { placement: 'bottom', label: 'Days' },
      yAxis: { placement: 'left', label: 'Return %' }
    }}
  />
</div>
