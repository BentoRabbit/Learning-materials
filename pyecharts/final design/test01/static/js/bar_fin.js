var dataMap = {};
function dataFormatter(obj) {
  // prettier-ignore
  var pList = ["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Hangzhou",];
  var temp;
  for (var year = 2018; year <= 2021; year++) {
    var max = 0;
    var sum = 0;
    temp = obj[year];
    for (var i = 0, l = temp.length; i < l; i++) {
      max = Math.max(max, temp[i]);
      sum += temp[i];
      obj[year][i] = {
        name: pList[i],
        value: temp[i]
      };
    }
    obj[year + 'max'] = Math.floor(max / 100) * 100;
    obj[year + 'sum'] = sum;
  }
  return obj;
}

// prettier-ignore
dataMap.dataPI = dataFormatter({
    //max : 4000,
    2021: [
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2021).filter(city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2021).filter(city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2021).filter(city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2021).filter(city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2021).filter(city1="Hangzhou").count(),
        ],
        2020: [
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2020).filter(city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2020).filter(city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2020).filter(city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2020).filter(city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2020).filter(city1="Hangzhou").count(),
        ],
        2019: [
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2019).filter(city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2019).filter(city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2019).filter(city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2019).filter(city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2019).filter(city1="Hangzhou").count(),
        ],
        2018: [
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2018).filter(city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2018).filter(city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2018).filter(city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2018).filter(city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=2018).filter(city1="Hangzhou").count(),

        ],});
// prettier-ignore
dataMap.dataSI = dataFormatter({
    //max : 26600,
    2021: [
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2021).filter(
                city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2021).filter(
                city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2021).filter(
                city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2021).filter(
                city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2021).filter(
                city1="Hangzhou").count(),
        ],
        2020: [
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2020).filter(
                city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2020).filter(
                city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2020).filter(
                city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2020).filter(
                city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2020).filter(
                city1="Hangzhou").count(),
        ],
        2019: [
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2019).filter(
                city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2019).filter(
                city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2019).filter(
                city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2019).filter(
                city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2019).filter(
                city1="Hangzhou").count(),
        ],
        2018: [
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2018).filter(
                city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2018).filter(
                city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2018).filter(
                city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2018).filter(
                city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=2018).filter(
                city1="Hangzhou").count(),
        ],});
// prettier-ignore
dataMap.dataTI = dataFormatter({
    //max : 25000,
    2021: [
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2021).filter(city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2021).filter(city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2021).filter(city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2021).filter(city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2021).filter(city1="Hangzhou").count(),
        ],
        2020: [
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2020).filter(city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2020).filter(city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2020).filter(city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2020).filter(city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2020).filter(city1="Hangzhou").count(),

        ],
        2019: [
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2019).filter(city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2019).filter(city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2019).filter(city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2019).filter(city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2019).filter(city1="Hangzhou").count(),
        ],
        2018: [
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2018).filter(city1="Shanghai").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2018).filter(city1="Beijing").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2018).filter(city1="Guangzhou").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2018).filter(city1="Chengdu").count(),
            Clinicaltrial.objects.filter(registry="EU-CTR").filter(start_year=2018).filter(city1="Hangzhou").count(),
        ],});

option = {
  baseOption: {
    timeline: {
      axisType: 'category',
      // realtime: false,
      // loop: false,
      autoPlay: true,
      // currentIndex: 2,
      playInterval: 1000,
      // controlStyle: {
      //     position: 'left'
      // },
      data: [
        '2018-01-01',
        '2019-01-01',
        '2020-01-01',
        {
          value: '2021-01-01',
          tooltip: {
            formatter: '{b} GDP达到一个高度'
          },
          symbol: 'diamond',
          symbolSize: 16
        }
      ],
      label: {
        formatter: function (s) {
          return new Date(s).getFullYear();
        }
      }
    },
    title: {
      subtext: '数据来自xxx'
    },
    tooltip: {},
    legend: {
      left: 'right',
      data: ['第一产业', '第二产业', '第三产业'],
    },
    calculable: true,
    grid: {
      top: 80,
      bottom: 100,
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
          label: {
            show: true,
            formatter: function (params) {
              return params.value.replace('\n', '');
            }
          }
        }
      }
    },
    xAxis: [
      {
        type: 'category',
        axisLabel: { interval: 0 },
        data: [
          'Shanghai',
          'Beijing',
          'Guangzhou',
          'Chendu',
          'Hangzhou'
        ],
        splitLine: { show: false }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: 'number（个）'
      }
    ],
    series: [
      { name: '第一产业', type: 'bar' },
      { name: '第二产业', type: 'bar' },
      { name: '第三产业', type: 'bar' },
      {
        name: '数量占比',
        type: 'pie',
        center: ['75%', '35%'],
        radius: '28%',
        z: 100
      }
    ]
  },
  options: [
    {
      title: { text: '2018全国宏观经济指标' },
      series: [
        { data: dataMap.dataPI['2018'] },
        { data: dataMap.dataSI['2018'] },
        { data: dataMap.dataTI['2018'] },
        {
          data: [
            { name: '第一产业', value: dataMap.dataPI['2018sum'] },
            { name: '第二产业', value: dataMap.dataSI['2018sum'] },
            { name: '第三产业', value: dataMap.dataTI['2018sum'] }
          ]
        }
      ]
    },
    {
      title: { text: '2019全国宏观经济指标' },
      series: [
        { data: dataMap.dataPI['2019'] },
        { data: dataMap.dataSI['2019'] },
        { data: dataMap.dataTI['2019'] },
        {
          data: [
            { name: '第一产业', value: dataMap.dataPI['2019sum'] },
            { name: '第二产业', value: dataMap.dataSI['2019sum'] },
            { name: '第三产业', value: dataMap.dataTI['2019sum'] }
          ]
        }
      ]
    },
    {
      title: { text: '2020全国宏观经济指标' },
      series: [
        { data: dataMap.dataPI['2020'] },
        { data: dataMap.dataSI['2020'] },
        { data: dataMap.dataTI['2020'] },
        {
          data: [
            { name: '第一产业', value: dataMap.dataPI['2020sum'] },
            { name: '第二产业', value: dataMap.dataSI['2020sum'] },
            { name: '第三产业', value: dataMap.dataTI['2020sum'] }
          ]
        }
      ]
    },
    {
      title: { text: '2021全国宏观经济指标' },
      series: [
        { data: dataMap.dataPI['2021'] },
        { data: dataMap.dataSI['2021'] },
        { data: dataMap.dataTI['2021'] },
        {
          data: [
            { name: '第一产业', value: dataMap.dataPI['2021sum'] },
            { name: '第二产业', value: dataMap.dataSI['2021sum'] },
            { name: '第三产业', value: dataMap.dataTI['2021sum'] }
          ]
        }
      ]
    }
  ]
};