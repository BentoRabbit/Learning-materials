


/*设置时间*/
setTime();
setInterval("setTime()", 1000);

// 补0 
function bu0(n) {
	return n < 10 ? '0' + n : n;
}

// 设置当前时间
function setTime() {
	var time = document.querySelector("#time");
	var myDate = new Date();
	time.innerHTML = myDate.getFullYear() + "-" + bu0((myDate.getMonth()+1)) + "-" + bu0(myDate.getDate()) + " " + bu0(myDate.getHours()) + ":" + bu0(myDate.getMinutes()) + ":" + bu0(myDate.getSeconds());
}










/*轮播图*/

//  轮播图当前播放索引
var slide_current = 0;

// 切换时间 毫秒
var slide_change_time = 3000;

// 轮播图item集合
var slide_divs = document.querySelectorAll(".slide-item");

// 添加轮播图索引小图标
for(var i = 0; i<slide_divs.length; i++) {
	var index_span = document.createElement("span");//创建一个标签
	if(i == 0){
		index_span.classList.add("active");
	}
	index_span.setAttribute("data-index", i);// 添加自定义属性
	index_span.addEventListener('click', function(){
		slide_current = this.getAttribute("data-index");
		slide_change(slide_current);
	});
	document.getElementById("pagination").append(index_span);
}

// 索引小图标集合
var pagination_spans = document.querySelectorAll("#pagination span");


/*定时器，第三个参数是第一个函数的参数*/
var interval = setInterval(slide_control, slide_change_time, "next");

/**
 * 轮播图控制
 * @param {Object} operation 
 */
function slide_control(operation) {
	
    if(operation == "prev") {
    	
    	if(slide_current == 0) {
    		// 已经是第一页了
    		slide_current = slide_divs.length-1;
    	} else {
    		slide_current--;
    	}
    	
    	
    } else if(operation == "next") {
    	
    	if(slide_current == slide_divs.length-1) {
    		// 已经是最后一页了
    		slide_current=0;
    	} else {
    		slide_current++;
    	}
    	
    }
    
    slide_change(slide_current);
    
}


function slide_change(index) {
	
	for(var i = 0; i < slide_divs.length; i++){ 
    	
    	if(slide_current == i) {
    		// 当前索引
    		slide_divs[i].style.display = 'block';
    		pagination_spans[i].classList.add("active");
    		
    	} else {
    		// 隐藏
    		slide_divs[i].style.display = 'none';
    		pagination_spans[i].classList.remove("active");
    	}
    	
    }
    
    // 先关闭再开启，避免点击切换时定时器立即又切换一张
    clearInterval(interval);
	interval = setInterval(slide_control, slide_change_time, "next");
    
	
	
}


