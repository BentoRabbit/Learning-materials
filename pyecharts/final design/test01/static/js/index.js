// 预警
(function() {

    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#warning1"));
    // 2. 指定配置项和数据
    // 数据及颜色设置
    let circleColor = '#0075ff'; // 三个圆环的颜色
    let gradientColor = ['#000204', '#0A2E6A']; // 中心圆渐变色
    let color = ['#2EB2FA', '#03FEFC', '#FFDF00', '#FFA8A8']; // 数据图表颜色数组
    let scale = 1;
    let echartData = [{
            name: 'A类',
            value: 30,
            unit: '个'
        },
        {
            name: 'B类',
            value: 20,
            unit: '个'
        }, {
            name: 'C类',
            value: 15,
            unit: '个'
        }
    ];
    let total = echartData.reduce((a, b) => {
        return a + b.value * 1
    }, 0)


    option = {
        color: color,
        title: {
            text: '异常分布情况',
            x: 135,
            y: 140,
            textStyle: {
                fontWeight: 'normal',
                fontSize: 13 * scale, //饼图内部文字大小
                color: "#fff",
            }
        },
        tooltip: {
            show: false
        },
        legend: {
            icon: 'rect',
            itemWidth: 14 * scale, //右侧图形宽度
            itemHeight: 14 * scale, //右侧图形高度
            orient: 'vertical',
            top: 80,
            right: 30,
            formatter: function(name) {
                let res = echartData.filter(v => v.name === name);
                res = res[0];
                let percent = (res.value * 100 / total).toFixed(2);
                return '{percent|' + percent + '}{unit| %}\n' + res.name + '{value|' + res.value + '}' + (res.unit || '')
            },
            textStyle: {
                color: '#fff',
                fontSize: 14 * scale,
                align: 'right',
                padding: [0, 0, 10 * scale, 0],
                rich: {
                    percent: {
                        fontSize: 16 * scale, //百分比数字大小
                        color: '#ffe400',
                        align: 'right'
                    },
                    unit: {
                        fontSize: 16 * scale, //百分比符号大小
                        align: 'right',
                        padding: [0, 0, 4 * scale, 0]
                    },
                    value: {
                        fontSize: 14 * scale, //数字大小
                        align: 'right',
                        padding: [0, 5 * scale, 0, 30 * scale]
                    }
                }
            }
        },
        series: [{
                type: 'pie',
                name: '最内层径向渐变圆心',
                clockWise: false,
                radius: '40%',
                center: ['40%', '60%'],
                z: 1,
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.RadialGradient(.5, .5, .6, [{
                                offset: 0,
                                color: gradientColor[0]
                            },
                            {
                                offset: 1,
                                color: gradientColor[1] || bgColor
                            }
                        ], false)
                    },
                },
                hoverAnimation: false,
                label: {
                    show: false,
                },
                tooltip: {
                    show: false
                },
                data: [100],
            },
            {
                type: 'pie',
                name: '内层细圆环1',
                radius: ['40%', '40%'],
                center: ['40%', '60%'],
                hoverAnimation: false,
                clockWise: false,
                itemStyle: {
                    normal: {
                        borderColor: circleColor,
                        borderWidth: 1,
                    }
                },
                label: {
                    show: false
                },
                data: [100]
            },
            {
                type: 'pie',
                name: '内层细圆环2',
                radius: ['45%', '46%'],
                center: ['40%', '60%'],
                hoverAnimation: false,
                clockWise: false,
                itemStyle: {
                    normal: {
                        borderColor: circleColor,
                        borderWidth: 1,
                    }
                },
                label: {
                    show: false
                },
                data: [100]
            },
            {
                type: 'pie',
                name: '最外层细圆环',
                hoverAnimation: false,
                clockWise: false,
                radius: ['60%', '61%'],
                center: ['40%', '60%'],
                itemStyle: {
                    normal: {
                        borderColor: circleColor,
                        borderWidth: 1,
                    }
                },
                label: {
                    show: false
                },
                data: [100]
            },
            {
                name: '饼图内容区',
                type: 'pie',
                clockWise: false,
                radius: ['47%', '59%'],
                center: ['40%', '60%'],
                hoverAnimation: false,
                data: echartData,
                itemStyle: {
                    normal: {
                        shadowBlur: 20,
                        shadowColor: '#00204',
                    }
                },
                label: {
                    show: false
                }
            }
        ]
    };


    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// 连接数
(function() {
    var MyMarhq = '';
    clearInterval(MyMarhq);
    $('.tbl-body tbody').empty();
    $('.tbl-header tbody').empty();
    var str = '';
    var Items = [{
        "level": "A",
        "ip": "194.255.16",
        "content": "720万"
    }, {
        "level": "B",
        "ip": "194.255.16",
        "content": "320万"
    }, {
        "level": "A",
        "ip": "194.255.16",
        "content": "300万"
    }, {
        "level": "A",
        "ip": "194.255.16",
        "content": "270万"
    }, {
        "level": "C",
        "ip": "194.255.16",
        "content": "720万"
    }, {
        "level": "A",
        "ip": "194.255.16",
        "content": "370万"
    }, {
        "level": "A",
        "ip": "194.255.16",
        "content": "360万"
    }, {
        "level": "B",
        "ip": "194.255.16",
        "content": "300万"
    }, {
        "level": "B",
        "ip": "194.255.16",
        "content": "110万"
    }, {
        "level": "C",
        "ip": "194.255.16",
        "content": "220万"
    }, {
        "level": "A",
        "ip": "194.255.16",
        "content": "350万"
    }]
    $.each(Items, function(i, item) { //each遍历数组元素
        str = '<tr>' +
            '<td>' + item.level + '</td>' +
            '<td>' + item.ip + '</td>' +
            '<td>' + item.content + '</td>' +
            '</tr>'

        $('.tbl-body tbody').append(str);
        $('.tbl-header tbody').append(str);
    });

    if (Items.length > 10) {
        $('.tbl-body tbody').html($('.tbl-body tbody').html() + $('.tbl-body tbody').html());
        $('.tbl-body').css('top', '0');
        var tblTop = 0;
        var speedhq = 30; // 数值越大越慢
        var outerHeight = $('.tbl-body tbody').find("tr").outerHeight(); //outerHeight()--返回 <div> 元素的外部高度,find()--方法获得当前元素集合中每个元素的后代

        function Marqueehq() {
            if (tblTop <= -outerHeight * Items.length) {
                tblTop = 0;
            } else {
                tblTop -= 1;
            }
            $('.tbl-body').css('top', tblTop + 'px');
        }

        MyMarhq = setInterval(Marqueehq, speedhq);

        // 鼠标移上去取消事件
        $(".tbl-header tbody").hover(function() {
            clearInterval(MyMarhq);
        }, function() {
            clearInterval(MyMarhq);
            MyMarhq = setInterval(Marqueehq, speedhq);
        })
    }
})();


// 数据库繁忙度
(function() {

    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#database2"));
    // 2. 指定配置项和数据
    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                lineStyle: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(0, 255, 233,0)'
                        }, {
                            offset: 0.5,
                            color: 'rgba(255, 255, 255,1)',
                        }, {
                            offset: 1,
                            color: 'rgba(0, 255, 233,0)'
                        }],
                        global: false
                    }
                },
            },
        },
        grid: {
            top: '15%',
            left: '10%',
            right: '10%',
            bottom: '10%',
            // containLabel: true
        },
        xAxis: [{
            type: 'category',
            axisLine: {
                show: true,
                color: '#A582EA'
            },

            axisLabel: {
                color: '#A582EA',
                width: 10
            },
            splitLine: {
                show: false
            },
            boundaryGap: false,
            data: ["8:00", "10:00", "12:00", "14:00", "16:00", "18:00", '20:00', '22:00', '24:00'] //this.$moment(data.times).format("HH-mm") ,

        }],

        yAxis: [{
            type: 'value',
            min: 0,
            // max: 140,
            splitNumber: 4,
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#00BFF3',
                    opacity: 0.23
                }
            },
            axisLine: {
                show: true,
            },
            axisLabel: {
                show: true,
                margin: 20,
                textStyle: {
                    color: '#fff',

                },
            },
            axisTick: {
                show: false,
            },
        }],
        series: [{
                name: '液压异常报警',
                type: 'line',
                showAllSymbol: true,
                symbol: 'circle',
                symbolSize: 10,
                lineStyle: {
                    normal: {
                        color: "#A582EA",
                    },
                },
                label: {
                    show: true,
                    position: 'top',
                    textStyle: {
                        color: '#A582EA',
                    }
                },
                itemStyle: {
                    color: "#fff",
                    borderColor: "#A582EA",
                    borderWidth: 2,
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(43,193,145,0.3)'
                            },
                            {
                                offset: 1,
                                color: 'rgba(43,193,145,0)'
                            }
                        ], false),
                    }
                },
                data: [4, 7, 5, 4, 3, 5, 8, 3, 4] //data.values
            },
            {
                name: '液位异常报警',
                type: 'line',
                showAllSymbol: true,
                symbol: 'circle',
                symbolSize: 10,
                lineStyle: {
                    normal: {
                        color: "#2CABE3",
                    },
                },
                label: {
                    show: true,
                    position: 'top',
                    textStyle: {
                        color: '#2CABE3',
                    }
                },
                itemStyle: {
                    color: "#fff",
                    borderColor: "#2CABE3",
                    borderWidth: 2,
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(81,150,164,0.3)'
                            },
                            {
                                offset: 1,
                                color: 'rgba(81,150,164,0)'
                            }
                        ], false),
                    }
                },
                data: [3, 5, 4, 2, 1, 7, 6, 8, 5] //data.values
            },
        ]
    };


    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// 归档
(function() {

    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#archive2"));
    // 2. 指定配置项和数据
    option = {
        tooltip: {
            trigger: "axis"
        },
        legend: {
            top: "0%",
            data: ["A", "B", "C"],
            textStyle: {
                color: "rgba(255,255,255,.5)",
                fontSize: "12"
            }
        },

        grid: {
            left: "10",
            top: "30",
            right: "15",
            bottom: "10",
            containLabel: true
        },
        xAxis: [{
            type: "category",
            boundaryGap: false,
            // x轴更换数据
            data: [
                "周一",
                "周二",
                "周三",
                "周四",
                "周五",
                "周六",
                "周日"
            ],
            // 文本颜色为rgba(255,255,255,.6)  文字大小为 12
            axisLabel: {
                textStyle: {
                    color: "rgba(255,255,255,.6)",
                    fontSize: 12
                }
            },
            // x轴线的颜色为   rgba(255,255,255,.2)
            axisLine: {
                lineStyle: {
                    color: "rgba(255,255,255,.2)"
                }
            }
        }],
        yAxis: [{
            type: "value",
            axisTick: { show: false },
            axisLine: {
                lineStyle: {
                    color: "rgba(255,255,255,.1)"
                }
            },
            axisLabel: {
                textStyle: {
                    color: "rgba(255,255,255,.6)",
                    fontSize: 12
                }
            },
            // 修改分割线的颜色
            splitLine: {
                lineStyle: {
                    color: "rgba(255,255,255,.1)"
                }
            }
        }],
        series: [{
                name: "A",
                type: "line",
                smooth: true,
                // 单独修改当前线条的样式
                lineStyle: {
                    color: "#0184d5",
                    width: "2"
                },
                // 填充颜色设置
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(
                        0,
                        0,
                        0,
                        1, [{
                                offset: 0,
                                color: "rgba(1, 132, 213, 0.4)" // 渐变色的起始颜色
                            },
                            {
                                offset: 0.8,
                                color: "rgba(1, 132, 213, 0.1)" // 渐变线的结束颜色
                            }
                        ],
                        false
                    ),
                    shadowColor: "rgba(0, 0, 0, 0.1)"
                },
                // 设置拐点
                symbol: "circle",
                // 拐点大小
                symbolSize: 8,
                // 开始不显示拐点， 鼠标经过显示
                showSymbol: false,
                // 设置拐点颜色以及边框
                itemStyle: {
                    color: "#0184d5",
                    borderColor: "rgba(221, 220, 107, .1)",
                    borderWidth: 12
                },
                data: [
                    30,
                    40,
                    30,
                    40,
                    30,
                    40,
                    30
                ]
            },
            {
                name: "B",
                type: "line",
                smooth: true,
                // 单独修改当前线条的样式
                lineStyle: {
                    color: "#FFDF00",
                    width: "2"
                },
                // 填充颜色设置
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(
                        0,
                        0,
                        0,
                        1, [{
                                offset: 0,
                                color: "rgba(255, 255, 0, 0.2)" // 渐变色的起始颜色
                            },
                            {
                                offset: 0.8,
                                color: "rgba(255, 255, 0, 0.1)" // 渐变线的结束颜色
                            }
                        ],
                        false
                    ),
                    shadowColor: "rgba(0, 0, 0, 0.1)"
                },
                // 设置拐点
                symbol: "circle",
                // 拐点大小
                symbolSize: 8,
                // 开始不显示拐点， 鼠标经过显示
                showSymbol: false,
                // 设置拐点颜色以及边框
                itemStyle: {
                    color: "#FFDF00",
                    borderColor: "rgba(221, 220, 107, .1)",
                    borderWidth: 12
                },
                data: [
                    18,
                    56,
                    42,
                    31,
                    19,
                    78,
                    30
                ]
            },
            {
                name: "C",
                type: "line",
                smooth: true,
                lineStyle: {
                    normal: {
                        color: "#00d887",
                        width: 2
                    }
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(
                            0,
                            0,
                            0,
                            1, [{
                                    offset: 0,
                                    color: "rgba(0, 216, 135, 0.4)"
                                },
                                {
                                    offset: 0.8,
                                    color: "rgba(0, 216, 135, 0.1)"
                                }
                            ],
                            false
                        ),
                        shadowColor: "rgba(0, 0, 0, 0.1)"
                    }
                },
                // 设置拐点 小圆点
                symbol: "circle",
                // 拐点大小
                symbolSize: 5,
                // 设置拐点颜色以及边框
                itemStyle: {
                    color: "#00d887",
                    borderColor: "rgba(221, 220, 107, .1)",
                    borderWidth: 12
                },
                // 开始不显示拐点， 鼠标经过显示
                showSymbol: false,
                data: [
                    130,
                    10,
                    20,
                    40,
                    30,
                    40,
                    80
                ]
            }
        ]
    };

    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// A水位图1
(function() {

    var value = 0.2;
    var data = [value, value, value, ];
    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down11111"));
    // 2. 指定配置项和数据
    option = {

        title: {
            text: (value * 100).toFixed(0) + '{a|%}',
            textStyle: {
                fontSize: 10,
                fontFamily: 'Microsoft Yahei',
                fontWeight: 'normal',
                color: '#FFFF00',
                rich: {
                    a: {
                        fontSize: 10,
                    }
                }
            },
            x: 'center',
            y: '35%'
        },
        graphic: [{
            type: 'group',
            left: 'center',
            top: '60%',
            children: [{
                type: 'text',
                z: 100,
                left: '10',
                top: 'middle',
                style: {
                    fill: '#fff',
                    text: 'CPU',
                    font: '10px  Microsoft YaHei'
                }
            }]
        }],
        series: [{
            type: 'liquidFill',
            radius: '80%',
            center: ['50%', '50%'],
            //  shape: 'roundRect',
            data: data,
            backgroundStyle: {
                color: {
                    type: 'linear',
                    x: 1,
                    y: 0,
                    x2: 0.5,
                    y2: 1,
                    colorStops: [{
                        offset: 1,
                        color: 'rgba(68, 145, 253, 0)'
                    }, {
                        offset: 0.5,
                        color: 'rgba(68, 145, 253, .25)'
                    }, {
                        offset: 0,
                        color: 'rgba(68, 145, 253, 1)'
                    }],
                    globalCoord: false
                },
            },
            outline: {
                borderDistance: 0,
                itemStyle: {
                    borderWidth: 10,
                    borderColor: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(69, 73, 240, 0)'
                        }, {
                            offset: 0.5,
                            color: 'rgba(69, 73, 240, .25)'
                        }, {
                            offset: 1,
                            color: 'rgba(69, 73, 240, 1)'
                        }],
                        globalCoord: false
                    },
                    shadowBlur: 10,
                    shadowColor: '#000',
                }
            },
            color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                    offset: 1,
                    color: 'rgba(58, 71, 212, 0)'
                }, {
                    offset: 0.5,
                    color: 'rgba(31, 222, 225, .2)'
                }, {
                    offset: 0,
                    color: 'rgba(31, 222, 225, 1)'
                }],
                globalCoord: false
            },
            label: {
                normal: {
                    formatter: '',
                }
            }
        }, ]
    };

    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// A水位图2
(function() {

    var value = 0.2;
    var data = [value, value, value, ];
    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down11112"));
    // 2. 指定配置项和数据
    option = {

        title: {
            text: (value * 100).toFixed(0) + '{a|%}',
            textStyle: {
                fontSize: 10,
                fontFamily: 'Microsoft Yahei',
                fontWeight: 'normal',
                color: '#FFFF00',
                rich: {
                    a: {
                        fontSize: 10,
                    }
                }
            },
            x: 'center',
            y: '35%'
        },
        graphic: [{
            type: 'group',
            left: 'center',
            top: '60%',
            children: [{
                type: 'text',
                z: 100,
                left: '10',
                top: 'middle',
                style: {
                    fill: '#FFF',
                    text: '内存',
                    font: '10px Microsoft YaHei'
                }
            }]
        }],
        series: [{
            type: 'liquidFill',
            radius: '80%',
            center: ['50%', '50%'],
            //  shape: 'roundRect',
            data: data,
            backgroundStyle: {
                color: {
                    type: 'linear',
                    x: 1,
                    y: 0,
                    x2: 0.5,
                    y2: 1,
                    colorStops: [{
                        offset: 1,
                        color: 'rgba(68, 145, 253, 0)'
                    }, {
                        offset: 0.5,
                        color: 'rgba(68, 145, 253, .25)'
                    }, {
                        offset: 0,
                        color: 'rgba(68, 145, 253, 1)'
                    }],
                    globalCoord: false
                },
            },
            outline: {
                borderDistance: 0,
                itemStyle: {
                    borderWidth: 10,
                    borderColor: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(69, 73, 240, 0)'
                        }, {
                            offset: 0.5,
                            color: 'rgba(69, 73, 240, .25)'
                        }, {
                            offset: 1,
                            color: 'rgba(69, 73, 240, 1)'
                        }],
                        globalCoord: false
                    },
                    shadowBlur: 10,
                    shadowColor: '#000',
                }
            },
            color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                    offset: 1,
                    color: 'rgba(58, 71, 212, 0)'
                }, {
                    offset: 0.5,
                    color: 'rgba(31, 222, 225, .2)'
                }, {
                    offset: 0,
                    color: 'rgba(31, 222, 225, 1)'
                }],
                globalCoord: false
            },
            label: {
                normal: {
                    formatter: '',
                }
            }
        }, ]
    };

    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// B水位图1
(function() {

    var value = 0.2;
    var data = [value, value, value, ];
    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down22211"));
    // 2. 指定配置项和数据
    option = {

        title: {
            text: (value * 100).toFixed(0) + '{a|%}',
            textStyle: {
                fontSize: 10,
                fontFamily: 'Microsoft Yahei',
                fontWeight: 'normal',
                color: '#FFFF00',
                rich: {
                    a: {
                        fontSize: 10,
                    }
                }
            },
            x: 'center',
            y: '35%'
        },
        graphic: [{
            type: 'group',
            left: 'center',
            top: '60%',
            children: [{
                type: 'text',
                z: 100,
                left: '10',
                top: 'middle',
                style: {
                    fill: '#FFF',
                    text: 'CPU',
                    font: '10px Microsoft YaHei'
                }
            }]
        }],
        series: [{
            type: 'liquidFill',
            radius: '80%',
            center: ['50%', '50%'],
            //  shape: 'roundRect',
            data: data,
            backgroundStyle: {
                color: {
                    type: 'linear',
                    x: 1,
                    y: 0,
                    x2: 0.5,
                    y2: 1,
                    colorStops: [{
                        offset: 1,
                        color: 'rgba(68, 145, 253, 0)'
                    }, {
                        offset: 0.5,
                        color: 'rgba(68, 145, 253, .25)'
                    }, {
                        offset: 0,
                        color: 'rgba(68, 145, 253, 1)'
                    }],
                    globalCoord: false
                },
            },
            outline: {
                borderDistance: 0,
                itemStyle: {
                    borderWidth: 10,
                    borderColor: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(69, 73, 240, 0)'
                        }, {
                            offset: 0.5,
                            color: 'rgba(69, 73, 240, .25)'
                        }, {
                            offset: 1,
                            color: 'rgba(69, 73, 240, 1)'
                        }],
                        globalCoord: false
                    },
                    shadowBlur: 10,
                    shadowColor: '#000',
                }
            },
            color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                    offset: 1,
                    color: 'rgba(58, 71, 212, 0)'
                }, {
                    offset: 0.5,
                    color: 'rgba(31, 222, 225, .2)'
                }, {
                    offset: 0,
                    color: 'rgba(31, 222, 225, 1)'
                }],
                globalCoord: false
            },
            label: {
                normal: {
                    formatter: '',
                }
            }
        }, ]
    };

    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// B水位图2
(function() {

    var value = 0.2;
    var data = [value, value, value, ];
    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down22212"));
    // 2. 指定配置项和数据
    option = {

        title: {
            text: (value * 100).toFixed(0) + '{a|%}',
            textStyle: {
                fontSize: 10,
                fontFamily: 'Microsoft Yahei',
                fontWeight: 'normal',
                color: '#FFFF00',
                rich: {
                    a: {
                        fontSize: 10,
                    }
                }
            },
            x: 'center',
            y: '35%'
        },
        graphic: [{
            type: 'group',
            left: 'center',
            top: '60%',
            children: [{
                type: 'text',
                z: 100,
                left: '10',
                top: 'middle',
                style: {
                    fill: '#FFF',
                    text: '内存',
                    font: '10px Microsoft YaHei'
                }
            }]
        }],
        series: [{
            type: 'liquidFill',
            radius: '80%',
            center: ['50%', '50%'],
            //  shape: 'roundRect',
            data: data,
            backgroundStyle: {
                color: {
                    type: 'linear',
                    x: 1,
                    y: 0,
                    x2: 0.5,
                    y2: 1,
                    colorStops: [{
                        offset: 1,
                        color: 'rgba(68, 145, 253, 0)'
                    }, {
                        offset: 0.5,
                        color: 'rgba(68, 145, 253, .25)'
                    }, {
                        offset: 0,
                        color: 'rgba(68, 145, 253, 1)'
                    }],
                    globalCoord: false
                },
            },
            outline: {
                borderDistance: 0,
                itemStyle: {
                    borderWidth: 10,
                    borderColor: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(69, 73, 240, 0)'
                        }, {
                            offset: 0.5,
                            color: 'rgba(69, 73, 240, .25)'
                        }, {
                            offset: 1,
                            color: 'rgba(69, 73, 240, 1)'
                        }],
                        globalCoord: false
                    },
                    shadowBlur: 10,
                    shadowColor: '#000',
                }
            },
            color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                    offset: 1,
                    color: 'rgba(58, 71, 212, 0)'
                }, {
                    offset: 0.5,
                    color: 'rgba(31, 222, 225, .2)'
                }, {
                    offset: 0,
                    color: 'rgba(31, 222, 225, 1)'
                }],
                globalCoord: false
            },
            label: {
                normal: {
                    formatter: '',
                }
            }
        }, ]
    };

    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// C水位图1
(function() {

    var value = 0.2;
    var data = [value, value, value, ];
    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down33311"));
    // 2. 指定配置项和数据
    option = {

        title: {
            text: (value * 100).toFixed(0) + '{a|%}',
            textStyle: {
                fontSize: 10,
                fontFamily: 'Microsoft Yahei',
                fontWeight: 'normal',
                color: '#FFFF00',
                rich: {
                    a: {
                        fontSize: 10,
                    }
                }
            },
            x: 'center',
            y: '35%'
        },
        graphic: [{
            type: 'group',
            left: 'center',
            top: '60%',
            children: [{
                type: 'text',
                z: 100,
                left: '10',
                top: 'middle',
                style: {
                    fill: '#FFF',
                    text: 'CPU',
                    font: '10px Microsoft YaHei'
                }
            }]
        }],
        series: [{
            type: 'liquidFill',
            radius: '80%',
            center: ['50%', '50%'],
            //  shape: 'roundRect',
            data: data,
            backgroundStyle: {
                color: {
                    type: 'linear',
                    x: 1,
                    y: 0,
                    x2: 0.5,
                    y2: 1,
                    colorStops: [{
                        offset: 1,
                        color: 'rgba(68, 145, 253, 0)'
                    }, {
                        offset: 0.5,
                        color: 'rgba(68, 145, 253, .25)'
                    }, {
                        offset: 0,
                        color: 'rgba(68, 145, 253, 1)'
                    }],
                    globalCoord: false
                },
            },
            outline: {
                borderDistance: 0,
                itemStyle: {
                    borderWidth: 10,
                    borderColor: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(69, 73, 240, 0)'
                        }, {
                            offset: 0.5,
                            color: 'rgba(69, 73, 240, .25)'
                        }, {
                            offset: 1,
                            color: 'rgba(69, 73, 240, 1)'
                        }],
                        globalCoord: false
                    },
                    shadowBlur: 10,
                    shadowColor: '#000',
                }
            },
            color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                    offset: 1,
                    color: 'rgba(58, 71, 212, 0)'
                }, {
                    offset: 0.5,
                    color: 'rgba(31, 222, 225, .2)'
                }, {
                    offset: 0,
                    color: 'rgba(31, 222, 225, 1)'
                }],
                globalCoord: false
            },
            label: {
                normal: {
                    formatter: '',
                }
            }
        }, ]
    };

    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// C水位图2
(function() {

    var value = 0.2;
    var data = [value, value, value, ];
    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down33312"));
    // 2. 指定配置项和数据
    option = {

        title: {
            text: (value * 100).toFixed(0) + '{a|%}',
            textStyle: {
                fontSize: 10,
                fontFamily: 'Microsoft Yahei',
                fontWeight: 'normal',
                color: '#FFFF00',
                rich: {
                    a: {
                        fontSize: 10,
                    }
                }
            },
            x: 'center',
            y: '35%'
        },
        graphic: [{
            type: 'group',
            left: 'center',
            top: '60%',
            children: [{
                type: 'text',
                z: 100,
                left: '10',
                top: 'middle',
                style: {
                    fill: '#FFF',
                    text: '内存',
                    font: '10px Microsoft YaHei'
                }
            }]
        }],
        series: [{
            type: 'liquidFill',
            radius: '80%',
            center: ['50%', '50%'],
            //  shape: 'roundRect',
            data: data,
            backgroundStyle: {
                color: {
                    type: 'linear',
                    x: 1,
                    y: 0,
                    x2: 0.5,
                    y2: 1,
                    colorStops: [{
                        offset: 1,
                        color: 'rgba(68, 145, 253, 0)'
                    }, {
                        offset: 0.5,
                        color: 'rgba(68, 145, 253, .25)'
                    }, {
                        offset: 0,
                        color: 'rgba(68, 145, 253, 1)'
                    }],
                    globalCoord: false
                },
            },
            outline: {
                borderDistance: 0,
                itemStyle: {
                    borderWidth: 10,
                    borderColor: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(69, 73, 240, 0)'
                        }, {
                            offset: 0.5,
                            color: 'rgba(69, 73, 240, .25)'
                        }, {
                            offset: 1,
                            color: 'rgba(69, 73, 240, 1)'
                        }],
                        globalCoord: false
                    },
                    shadowBlur: 10,
                    shadowColor: '#000',
                }
            },
            color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                    offset: 1,
                    color: 'rgba(58, 71, 212, 0)'
                }, {
                    offset: 0.5,
                    color: 'rgba(31, 222, 225, .2)'
                }, {
                    offset: 0,
                    color: 'rgba(31, 222, 225, 1)'
                }],
                globalCoord: false
            },
            label: {
                normal: {
                    formatter: '',
                }
            }
        }, ]
    };

    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// D水位图1
(function() {

    var value = 0.2;
    var data = [value, value, value, ];
    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down44411"));
    // 2. 指定配置项和数据
    option = {

        title: {
            text: (value * 100).toFixed(0) + '{a|%}',
            textStyle: {
                fontSize: 10,
                fontFamily: 'Microsoft Yahei',
                fontWeight: 'normal',
                color: '#FFFF00',
                rich: {
                    a: {
                        fontSize: 10,
                    }
                }
            },
            x: 'center',
            y: '35%'
        },
        graphic: [{
            type: 'group',
            left: 'center',
            top: '60%',
            children: [{
                type: 'text',
                z: 100,
                left: '10',
                top: 'middle',
                style: {
                    fill: '#FFF',
                    text: 'CPU',
                    font: '10px Microsoft YaHei'
                }
            }]
        }],
        series: [{
            type: 'liquidFill',
            radius: '80%',
            center: ['50%', '50%'],
            //  shape: 'roundRect',
            data: data,
            backgroundStyle: {
                color: {
                    type: 'linear',
                    x: 1,
                    y: 0,
                    x2: 0.5,
                    y2: 1,
                    colorStops: [{
                        offset: 1,
                        color: 'rgba(68, 145, 253, 0)'
                    }, {
                        offset: 0.5,
                        color: 'rgba(68, 145, 253, .25)'
                    }, {
                        offset: 0,
                        color: 'rgba(68, 145, 253, 1)'
                    }],
                    globalCoord: false
                },
            },
            outline: {
                borderDistance: 0,
                itemStyle: {
                    borderWidth: 10,
                    borderColor: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(69, 73, 240, 0)'
                        }, {
                            offset: 0.5,
                            color: 'rgba(69, 73, 240, .25)'
                        }, {
                            offset: 1,
                            color: 'rgba(69, 73, 240, 1)'
                        }],
                        globalCoord: false
                    },
                    shadowBlur: 10,
                    shadowColor: '#000',
                }
            },
            color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                    offset: 1,
                    color: 'rgba(58, 71, 212, 0)'
                }, {
                    offset: 0.5,
                    color: 'rgba(31, 222, 225, .2)'
                }, {
                    offset: 0,
                    color: 'rgba(31, 222, 225, 1)'
                }],
                globalCoord: false
            },
            label: {
                normal: {
                    formatter: '',
                }
            }
        }, ]
    };

    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


// D水位图2
(function() {

    var value = 0.2;
    var data = [value, value, value, ];
    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down44412"));
    // 2. 指定配置项和数据
    option = {

        title: {
            text: (value * 100).toFixed(0) + '{a|%}',
            textStyle: {
                fontSize: 10,
                fontFamily: 'Microsoft Yahei',
                fontWeight: 'normal',
                color: '#FFFF00',
                rich: {
                    a: {
                        fontSize: 10,
                    }
                }
            },
            x: 'center',
            y: '35%'
        },
        graphic: [{
            type: 'group',
            left: 'center',
            top: '60%',
            children: [{
                type: 'text',
                z: 100,
                left: '10',
                top: 'middle',
                style: {
                    fill: '#FFF',
                    text: '内存',
                    font: '10px Microsoft YaHei'
                }
            }]
        }],
        series: [{
            type: 'liquidFill',
            radius: '80%',
            center: ['50%', '50%'],
            //  shape: 'roundRect',
            data: data,
            backgroundStyle: {
                color: {
                    type: 'linear',
                    x: 1,
                    y: 0,
                    x2: 0.5,
                    y2: 1,
                    colorStops: [{
                        offset: 1,
                        color: 'rgba(68, 145, 253, 0)'
                    }, {
                        offset: 0.5,
                        color: 'rgba(68, 145, 253, .25)'
                    }, {
                        offset: 0,
                        color: 'rgba(68, 145, 253, 1)'
                    }],
                    globalCoord: false
                },
            },
            outline: {
                borderDistance: 0,
                itemStyle: {
                    borderWidth: 10,
                    borderColor: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(69, 73, 240, 0)'
                        }, {
                            offset: 0.5,
                            color: 'rgba(69, 73, 240, .25)'
                        }, {
                            offset: 1,
                            color: 'rgba(69, 73, 240, 1)'
                        }],
                        globalCoord: false
                    },
                    shadowBlur: 10,
                    shadowColor: '#000',
                }
            },
            color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                    offset: 1,
                    color: 'rgba(58, 71, 212, 0)'
                }, {
                    offset: 0.5,
                    color: 'rgba(31, 222, 225, .2)'
                }, {
                    offset: 0,
                    color: 'rgba(31, 222, 225, 1)'
                }],
                globalCoord: false
            },
            label: {
                normal: {
                    formatter: '',
                }
            }
        }, ]
    };

    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


//磁盘占用量A
(function() {

    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down1112"));
    // 2. 指定配置项和数据
    option = {
        grid: {
            top: "6%",
            bottom: "33%"
        },
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow",
                label: {
                    show: true
                }
            }
        },
        legend: {
            data: ["磁盘用量"],
            top: "0%",
            textStyle: {
                color: "#ffffff"
            }
        },
        xAxis: {
            data: ['A盘', 'B盘', 'C盘', 'D盘', 'E盘'],
            offset: 12,
            axisLine: {
                show: false,
            },
            axisLabel: {
                show: true,
                textStyle: {
                    fontSize: 10,
                    color: '#fff'
                }
            },
            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
        },
        yAxis: [{
                type: 'value',
                name: '(g)',
                min: 0,
                max: 400,
                axisLabel: {
                    formatter: '{value}',
                    textStyle: {
                        color: '#fff'
                    }
                },
                axisLine: {
                    show: false,
                    lineStyle: {
                        color: '#fff'
                    }
                },
                axisTick: {
                    show: false,

                },
                splitLine: {
                    show: false,
                    lineStyle: {
                        color: '#262b35'
                    }
                }
            },
            {
                type: "value",
                name: "同比",
                nameTextStyle: {
                    color: "#fff"
                },
                position: "right",
                splitLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                axisLabel: {
                    show: true,
                    formatter: '{value}%', //右侧Y轴文字显示
                    textStyle: {
                        color: "#fff"
                    }
                }
            },
            {
                type: "value",
                gridIndex: 0,
                min: 50,
                max: 100,
                splitNumber: 8,
                splitLine: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLabel: {
                    show: false
                },
                splitArea: {
                    show: true,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.0)", "rgba(250,250,250,0.05)"]
                    }
                }
            }
        ],
        series: [

            {
                type: 'bar',
                name: '磁盘用量',
                barWidth: 18,
                label: {
                    show: true,
                    position: 'top',
                    fontSize: 10,
                    color: '#fff'
                },
                emphasis: {
                    itemStyle: {
                        color: '#7fb7e9'
                    }
                },
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#00e4ec' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0946f1' // 100% 处的颜色
                        }], false),

                    }
                },
                data: [220, 182, 191, 234, 223]
            }, {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'bar',
                barWidth: 18,
                emphasis: {
                    itemStyle: {
                        color: '#2e9bff'
                    }
                },
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#00e4ec' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0946f1' // 100% 处的颜色
                        }], false),

                    }
                },
                data: [220, 182, 191, 234, 223],
                barGap: 0,
                legendHoverLink: false,
            }, {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'pictorialBar',

                itemStyle: {
                    normal: {
                        color: '#73bbff',
                        // borderWidth:1,
                        // borderColor:'#3c93fc'
                    }
                },

                symbolRotate: 0,
                symbolSize: ['36', '9'],
                symbolOffset: ['0', '4'],
                symbolPosition: 'start',
                data: [220, 182, 191, 234, 223],
                z: 3
            },
            {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'pictorialBar',
                itemStyle: {
                    normal: {
                        color: '#73bbff',
                        // borderWidth:1,
                        // borderColor:'#3c93fc'
                    }
                },


                symbolRotate: 0,
                symbolSize: ['36', '9'],
                symbolOffset: ['0', '-4'],
                symbolPosition: 'end',
                data: [220, 182, 191, 234, 223],
                z: 3
            },

        ]
    };
    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


//磁盘占用量B
(function() {

    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down2222"));
    // 2. 指定配置项和数据
    option = {
        grid: {
            top: "6%",
            bottom: "33%"
        },
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow",
                label: {
                    show: true
                }
            }
        },
        legend: {
            data: ["磁盘用量"],
            top: "0%",
            textStyle: {
                color: "#ffffff"
            }
        },
        xAxis: {
            data: ['A盘', 'B盘', 'C盘', 'D盘', 'E盘'],
            offset: 12,
            axisLine: {
                show: false,
            },
            axisLabel: {
                show: true,
                textStyle: {
                    fontSize: 10,
                    color: '#fff'
                }
            },
            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
        },
        yAxis: [{
                type: 'value',
                name: '(g)',
                min: 0,
                max: 400,
                axisLabel: {
                    formatter: '{value}',
                    textStyle: {
                        color: '#fff'
                    }
                },
                axisLine: {
                    show: false,
                    lineStyle: {
                        color: '#fff'
                    }
                },
                axisTick: {
                    show: false,

                },
                splitLine: {
                    show: false,
                    lineStyle: {
                        color: '#262b35'
                    }
                }
            },
            {
                type: "value",
                name: "同比",
                nameTextStyle: {
                    color: "#fff"
                },
                position: "right",
                splitLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                axisLabel: {
                    show: true,
                    formatter: '{value}%', //右侧Y轴文字显示
                    textStyle: {
                        color: "#fff"
                    }
                }
            },
            {
                type: "value",
                gridIndex: 0,
                min: 50,
                max: 100,
                splitNumber: 8,
                splitLine: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLabel: {
                    show: false
                },
                splitArea: {
                    show: true,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.0)", "rgba(250,250,250,0.05)"]
                    }
                }
            }
        ],
        series: [

            {
                type: 'bar',
                name: '磁盘用量',
                barWidth: 18,
                label: {
                    show: true,
                    position: 'top',
                    fontSize: 10,
                    color: '#fff'
                },
                emphasis: {
                    itemStyle: {
                        color: '#7fb7e9'
                    }
                },
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#00e4ec' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0946f1' // 100% 处的颜色
                        }], false),

                    }
                },
                data: [220, 182, 191, 234, 223]
            }, {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'bar',
                barWidth: 18,
                emphasis: {
                    itemStyle: {
                        color: '#2e9bff'
                    }
                },
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#00e4ec' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0946f1' // 100% 处的颜色
                        }], false),

                    }
                },
                data: [220, 182, 191, 234, 223],
                barGap: 0,
                legendHoverLink: false,
            }, {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'pictorialBar',

                itemStyle: {
                    normal: {
                        color: '#73bbff',
                        // borderWidth:1,
                        // borderColor:'#3c93fc'
                    }
                },

                symbolRotate: 0,
                symbolSize: ['36', '9'],
                symbolOffset: ['0', '4'],
                symbolPosition: 'start',
                data: [220, 182, 191, 234, 223],
                z: 3
            },
            {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'pictorialBar',
                itemStyle: {
                    normal: {
                        color: '#73bbff',
                        // borderWidth:1,
                        // borderColor:'#3c93fc'
                    }
                },


                symbolRotate: 0,
                symbolSize: ['36', '9'],
                symbolOffset: ['0', '-4'],
                symbolPosition: 'end',
                data: [220, 182, 191, 234, 223],
                z: 3
            },

        ]
    };
    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


//磁盘占用量C
(function() {

    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down3332"));
    // 2. 指定配置项和数据
    option = {
        grid: {
            top: "6%",
            bottom: "33%"
        },
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow",
                label: {
                    show: true
                }
            }
        },
        legend: {
            data: ["磁盘用量"],
            top: "0%",
            textStyle: {
                color: "#ffffff"
            }
        },
        xAxis: {
            data: ['A盘', 'B盘', 'C盘', 'D盘', 'E盘'],
            offset: 12,
            axisLine: {
                show: false,
            },
            axisLabel: {
                show: true,
                textStyle: {
                    fontSize: 10,
                    color: '#fff'
                }
            },
            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
        },
        yAxis: [{
                type: 'value',
                name: '(g)',
                min: 0,
                max: 400,
                axisLabel: {
                    formatter: '{value}',
                    textStyle: {
                        color: '#fff'
                    }
                },
                axisLine: {
                    show: false,
                    lineStyle: {
                        color: '#fff'
                    }
                },
                axisTick: {
                    show: false,

                },
                splitLine: {
                    show: false,
                    lineStyle: {
                        color: '#262b35'
                    }
                }
            },
            {
                type: "value",
                name: "同比",
                nameTextStyle: {
                    color: "#fff"
                },
                position: "right",
                splitLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                axisLabel: {
                    show: true,
                    formatter: '{value}%', //右侧Y轴文字显示
                    textStyle: {
                        color: "#fff"
                    }
                }
            },
            {
                type: "value",
                gridIndex: 0,
                min: 50,
                max: 100,
                splitNumber: 8,
                splitLine: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLabel: {
                    show: false
                },
                splitArea: {
                    show: true,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.0)", "rgba(250,250,250,0.05)"]
                    }
                }
            }
        ],
        series: [

            {
                type: 'bar',
                name: '磁盘用量',
                barWidth: 18,
                label: {
                    show: true,
                    position: 'top',
                    fontSize: 10,
                    color: '#fff'
                },
                emphasis: {
                    itemStyle: {
                        color: '#7fb7e9'
                    }
                },
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#00e4ec' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0946f1' // 100% 处的颜色
                        }], false),

                    }
                },
                data: [220, 182, 191, 234, 223]
            }, {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'bar',
                barWidth: 18,
                emphasis: {
                    itemStyle: {
                        color: '#2e9bff'
                    }
                },
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#00e4ec' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0946f1' // 100% 处的颜色
                        }], false),

                    }
                },
                data: [220, 182, 191, 234, 223],
                barGap: 0,
                legendHoverLink: false,
            }, {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'pictorialBar',

                itemStyle: {
                    normal: {
                        color: '#73bbff',
                        // borderWidth:1,
                        // borderColor:'#3c93fc'
                    }
                },

                symbolRotate: 0,
                symbolSize: ['36', '9'],
                symbolOffset: ['0', '4'],
                symbolPosition: 'start',
                data: [220, 182, 191, 234, 223],
                z: 3
            },
            {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'pictorialBar',
                itemStyle: {
                    normal: {
                        color: '#73bbff',
                        // borderWidth:1,
                        // borderColor:'#3c93fc'
                    }
                },


                symbolRotate: 0,
                symbolSize: ['36', '9'],
                symbolOffset: ['0', '-4'],
                symbolPosition: 'end',
                data: [220, 182, 191, 234, 223],
                z: 3
            },

        ]
    };
    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


//磁盘占用量D
(function() {

    // 1实例化对象
    var myChart = echarts.init(document.querySelector("#down4442"));
    // 2. 指定配置项和数据
    option = {
        grid: {
            top: "6%",
            bottom: "33%"
        },
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow",
                label: {
                    show: true
                }
            }
        },
        legend: {
            data: ["磁盘用量"],
            top: "0%",
            textStyle: {
                color: "#ffffff"
            }
        },
        xAxis: {
            data: ['A盘', 'B盘', 'C盘', 'D盘', 'E盘'],
            offset: 12,
            axisLine: {
                show: false,
            },
            axisLabel: {
                show: true,
                textStyle: {
                    fontSize: 10,
                    color: '#fff'
                }
            },
            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
        },
        yAxis: [{
                type: 'value',
                name: '(g)',
                min: 0,
                max: 400,
                axisLabel: {
                    formatter: '{value}',
                    textStyle: {
                        color: '#fff'
                    }
                },
                axisLine: {
                    show: false,
                    lineStyle: {
                        color: '#fff'
                    }
                },
                axisTick: {
                    show: false,

                },
                splitLine: {
                    show: false,
                    lineStyle: {
                        color: '#262b35'
                    }
                }
            },
            {
                type: "value",
                name: "同比",
                nameTextStyle: {
                    color: "#fff"
                },
                position: "right",
                splitLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                axisLabel: {
                    show: true,
                    formatter: '{value}%', //右侧Y轴文字显示
                    textStyle: {
                        color: "#fff"
                    }
                }
            },
            {
                type: "value",
                gridIndex: 0,
                min: 50,
                max: 100,
                splitNumber: 8,
                splitLine: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLabel: {
                    show: false
                },
                splitArea: {
                    show: true,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.0)", "rgba(250,250,250,0.05)"]
                    }
                }
            }
        ],
        series: [

            {
                type: 'bar',
                name: '磁盘用量',
                barWidth: 18,
                label: {
                    show: true,
                    position: 'top',
                    fontSize: 10,
                    color: '#fff'
                },
                emphasis: {
                    itemStyle: {
                        color: '#7fb7e9'
                    }
                },
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#00e4ec' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0946f1' // 100% 处的颜色
                        }], false),

                    }
                },
                data: [220, 182, 191, 234, 223]
            }, {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'bar',
                barWidth: 18,
                emphasis: {
                    itemStyle: {
                        color: '#2e9bff'
                    }
                },
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#00e4ec' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0946f1' // 100% 处的颜色
                        }], false),

                    }
                },
                data: [220, 182, 191, 234, 223],
                barGap: 0,
                legendHoverLink: false,
            }, {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'pictorialBar',

                itemStyle: {
                    normal: {
                        color: '#73bbff',
                        // borderWidth:1,
                        // borderColor:'#3c93fc'
                    }
                },

                symbolRotate: 0,
                symbolSize: ['36', '9'],
                symbolOffset: ['0', '4'],
                symbolPosition: 'start',
                data: [220, 182, 191, 234, 223],
                z: 3
            },
            {
                name: '磁盘用量',
                tooltip: {
                    show: false
                },
                type: 'pictorialBar',
                itemStyle: {
                    normal: {
                        color: '#73bbff',
                        // borderWidth:1,
                        // borderColor:'#3c93fc'
                    }
                },


                symbolRotate: 0,
                symbolSize: ['36', '9'],
                symbolOffset: ['0', '-4'],
                symbolPosition: 'end',
                data: [220, 182, 191, 234, 223],
                z: 3
            },

        ]
    };
    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();


//地图
(function() {
    var geoCoordMap = {
        '上海市区': [121.430317, 31.222771],
        '闵行区': [121.375972, 31.111658],
        '宝山区': [121.489934, 31.398896],
        '嘉定区': [121.250333, 31.383524],
        '浦东新区': [121.567706, 31.245944],
        '金山区': [121.330736, 30.724697],
        '松江区': [121.223543, 31.03047],
        '青浦区': [121.113021, 31.151209],
        '奉贤区': [121.458472, 30.912345],
        '崇明区': [121.397516, 31.626946],
    }
    var data = [{
            name: '上海市区',
            value: 985
        },
        {
            name: '闵行区',
            value: 470
        }, {
            name: '宝山区',
            value: 375
        }, {
            name: '嘉定区',
            value: 180
        }, {
            name: '浦东新区',
            value: 578
        }, {
            name: '金山区',
            value: 77
        }, {
            name: '松江区',
            value: 179
        }, {
            name: '青浦区',
            value: 285
        }, {
            name: '奉贤区',
            value: 181
        }, {
            name: '崇明区',
            value: 183
        }
    ];


    var convertData = function(data) {
        var res = [];
        for (var i = 0; i < data.length; i++) {
            var geoCoord = geoCoordMap[data[i].name];
            if (geoCoord) {
                res.push({
                    name: data[i].name,
                    value: geoCoord.concat(data[i].value)
                });
            }
        }
        return res;
    };

    //1.实例化对象
    var myChart = echarts.init(document.querySelector("#topMid11"));
    //2. 指定配置

    var option = {
        tooltip: {
            trigger: "none",
            show: true,
            padding: 0,
            backgroundColor: "#ffffff33",
            formatter: function(params, ticket, callback) {
                //根据业务自己拓展要显示的内容
                var res = "";
                var name = params.name;
                var color = params.color;
                res = "<span style='color:#fff;'>地址：" + name;
                return res;
            }
        },

        geo: {
            map: '上海',
            left: 'center',
            top: 'center',
            zoom: 1.2,
            roam: false,
            itemStyle: {
                normal: {
                    borderColor: 'rgba(147, 235, 248, 1)',
                    borderWidth: 1,
                    areaColor: {
                        type: 'radial',
                        x: 0.5,
                        y: 0.5,
                        r: 0.8,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(147, 235, 248, 0)' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: 'rgba(147, 235, 248, .2)' // 100% 处的颜色
                        }],
                        globalCoord: false // 缺省为 false
                    },
                    shadowColor: 'rgba(128, 217, 248, 1)',
                    // shadowColor: 'rgba(255, 255, 255, 1)',
                    shadowOffsetX: -2,
                    shadowOffsetY: 2,
                    shadowBlur: 10
                },
                emphasis: {
                    areaColor: '#389BB7',
                    borderWidth: 0
                }
            }
        },

        series: [{
                type: 'map',
                mapType: '上海',
                left: 'center',
                top: 'center',
                zoom: 1.2,
                roam: false, //是否开启鼠标缩放和平移漫游
                itemStyle: {
                    normal: {
                        borderColor: 'rgba(147, 235, 248, 1)',
                        borderWidth: 1,
                        areaColor: {
                            type: 'radial',
                            x: 0.5,
                            y: 0.5,
                            r: 0.8,
                            colorStops: [{
                                offset: 0,
                                color: 'rgba(147, 235, 248, 0)' // 0% 处的颜色
                            }, {
                                offset: 1,
                                color: 'rgba(147, 235, 248, .2)' // 100% 处的颜色
                            }],
                            globalCoord: false // 缺省为 false
                        },
                        shadowColor: 'rgba(128, 217, 248, 1)',
                        // shadowColor: 'rgba(255, 255, 255, 1)',
                        shadowOffsetX: -2,
                        shadowOffsetY: 2,
                        shadowBlur: 10
                    },
                    emphasis: {
                        areaColor: '#389BB7',
                        borderWidth: 0
                    }
                }
            },
            {
                name: '中心点显示按钮',
                type: 'effectScatter',
                right: '10',
                coordinateSystem: 'geo',
                data: convertData(data), //鼠标触发散点显示内容
                symbolSize: function(val) { //散点的尺寸
                    return val[1] / 10;
                },
                showEffectOn: 'render', //配置何时显示特效
                rippleEffect: {
                    brushType: 'stroke' //波纹的绘制方式
                },
                hoverAnimation: true, //是否在拐点标志上显示动画效果
                label: { //鼠标移动到此处显示的文字的样式
                    normal: {
                        formatter: '{b}',
                        position: 'bottom',
                        color: '#fff',
                        show: true
                    }
                },
                itemStyle: { //散点的颜色
                    normal: {
                        color: '#10f9ff',
                        shadowBlur: 0,
                        shadowColor: '#05C3F9'
                    }
                },
                zlevel: 1
            },
            {
                type: 'scatter',
                coordinateSystem: 'geo',
                zlevel: 0.9,
                symbolSize: [30, 30],
                symbol: 'path://M32 18.451l-16-12.42-16 12.42v-5.064l16-12.42 16 12.42zM28 18v12h-8v-8h-8v8h-8v-12l12-9z',
                data: [{
                    name: '金山区(DB2)',
                    value: [121.330736, 30.824697]
                }]
            },
            { //杨浦区
                type: 'scatter',
                coordinateSystem: 'geo',
                zlevel: 0.9,
                // symbolOffset: [15, -40],相对制定坐标移动相应距离
                symbolSize: [30, 30],
                symbol: 'path://M32 18.451l-16-12.42-16 12.42v-5.064l16-12.42 16 12.42zM28 18v12h-8v-8h-8v8h-8v-12l12-9z',
                data: [{
                    name: '杨树浦路(DB1)',
                    value: [121.54, 31.3595]
                }]

            },
            { //虹口区
                type: 'scatter',
                coordinateSystem: 'geo',
                zlevel: 0.9,
                // symbolOffset: [15, -40],相对制定坐标移动相应距离
                symbolSize: [30, 30],
                symbol: 'path://M32 18.451l-16-12.42-16 12.42v-5.064l16-12.42 16 12.42zM28 18v12h-8v-8h-8v8h-8v-12l12-9z',
                data: [{
                    name: '四平路(DB3)',
                    value: [121.44, 31.2595]
                }]

            },
            {
                name: '数据传输图',
                type: 'lines',
                coordinateSystem: 'geo',
                //polyline:true,
                symbol: ['none', 'triangle'],
                zlevel: 2,
                effect: {
                    show: true,
                    symbol: 'roundRect',
                    period: 2, //特效动画时间(s)
                    delay: 100, //特效动画延迟时间（ms）
                    trailLength: 0.5, //特效尾迹的长度。取从 0 到 1 的值，数值越大尾迹越长
                    symbolSize: 3, //特效标记大小
                },
                lineStyle: {
                    normal: {
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [{
                                offset: 0,
                                color: '#FFFF00'
                            }, {
                                offset: 1,
                                color: '#FFFF00'
                            }],
                            globalCoord: false
                        },
                        width: 0.05,
                        opacity: 0.8,
                        //type: 'dotted',
                        curveness: 0.5, //边的曲度，支持从 0 到 1 的值，值越大曲度越大
                    }
                },
                data: [{
                    coords: [ //杨--金
                        [121.54, 31.3595],
                        [121.330736, 30.824697],
                    ]
                }, {
                    coords: [ //金--四
                        [121.330736, 30.824697],
                        [121.44, 31.2595],
                    ]
                }, {
                    coords: [ //四--杨
                        [121.44, 31.2595],
                        [121.54, 31.3595],
                    ]
                }]
            }

        ]
    };
    // 3. 把配置项给实例对象
    myChart.setOption(option);
    // 4. 让图表跟随屏幕自动的去适应
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();