<template>
  <div class="righttop" ref="charts">
      
  </div>
</template>

<script>
import echarts from 'echarts'    //   npm install echarts@4.9.0
export default {
    name:"",
    data () {
        return {
            
        }
    },
    mounted () {
        this.mycharts()
    },
    methods: {
        mycharts(){
        let myChart =echarts.init(this.$refs.charts,"macarons");
            myChart.setOption(
                {
                    color:['rgb(8,252,7)','rgb(255,168,0)','rgb(0,121,254)','rgb(0,255,251)'],
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow',
                            crossStyle: {
                                color: '#999'
                            }
                        },
                        
                        position: function(pt) { //提示框的位置
                        return [pt[0], 30];
                        }
                    },
                     grid: { //图表和父盒子之间的距离
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        top:'17%',
                        containLabel: true
                    },
                    legend: {//图例
                        data: [
                            {
                                name:'完成值',
                                textStyle: {
                                    color: '#fff'
                                }
                            },
                            {
                                name: '计划值',
                                textStyle: {
                                    color: '#fff'
                                }
                            },
                            {
                                name: '同期值',
                                textStyle: {
                                    color: '#fff'
                                }
                            },{
                                name: '上期值',
                                textStyle: {
                                    color: '#fff'
                                }
                            }
                        ]
                    },
                    xAxis:{ //x轴
                            type: 'category',
                            // boundaryGap: false,
                            data: ['供电煤耗', '综合厂用电率', '发电厂用电率', '发电水耗率', '发电油耗率'],
                            axisLabel: { 
                                interval:0,
                                textStyle: {
                                color: '#fff',
                                    fontSize :10
                                },
                                margin:8
                            },
                            axisLine:{
                                show :true,
                                lineStyle:{
                                    color:'rgb(2,121,253)'
                                }
                            },
                            axisTick:{
                                show :false,
                            }
                        },
                    yAxis:{
                            type: 'value',
                             axisLabel: { //x轴的坐标文字
                            show: true,
                            textStyle: {
                                color: '#fff' //文字的颜色
                                },
                                
                            },
                            max:100,
                            axisLine:{
                                show :true,
                                lineStyle:{
                                    color:'rgb(2,121,253)'
                                }
                            },
                            axisTick:{
                                show :false,
                            },
                            splitLine:{  //坐标在grid区域的分割线
                            　 lineStyle: { //设置分割线的样式(图表横线颜色)
                                    color: ['#153a8a']
                                }
                            }
                    },
                    series: [
                        {
                            name: '完成值',
                            type: 'bar', //柱状图
                            data: [30,40,50,60,70],
                            barWidth :'8%' //柱状体的宽度
                        },
                        {
                            name: '计划值',
                            type: 'bar',
                            data: [20,50,60,40,40],
                            barWidth :'8%'  
                        },
                        {
                            name: '同期值',
                            type: 'bar',
                            data: [60,50,40,30,20],
                            barWidth :'8%'
                        },
                        {
                            name: '上期值',
                            type: 'bar',
                            data: [50,70,60,30,40],
                            barWidth :'8%',
                           
                        },
                    
                    ]
                }
            )
            //让图表自适应
            window.addEventListener("resize",function(){
                myChart.resize()  // myChart 是实例对象
            })
        }
    }
}
</script>

<style scoped>
.righttop{
    width: 100%;
	  height: 400px;
	  background: rgb(14, 51, 129);
}
</style>
