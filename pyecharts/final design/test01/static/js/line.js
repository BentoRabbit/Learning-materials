
option = {
  xAxis: {
    type: 'category',
    data: [2018,2019,2020,2021]
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [Clinicaltrial.objects.filter(start_year=2018).count(),Clinicaltrial.objects.filter(start_year=2019).count(),Clinicaltrial.objects.filter(start_year=2020).count(),Clinicaltrial.objects.filter(start_year=2021).count()],
      type: 'line',
      smooth: true
    }
  ]
};