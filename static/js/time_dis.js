let Week_opt = {
    "en": ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'],
    "cn": ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
}

Week = Week_opt[lan]

function getDate() {
    //获取当前时间
    let time_now = new Date();

    //格式化
    let year = time_now.getFullYear();
    let month = time_now.getMonth() + 1; month = month>9?month:"0"+month;
    let date = time_now.getDate(); date = date>9?date:"0"+date;
    let hours = time_now.getHours(); hours = hours>9?hours:"0"+hours;
    let minutes = time_now.getMinutes(); minutes = minutes>9?minutes:"0"+minutes;
    let seconds = time_now.getSeconds(); seconds = seconds>9?seconds:"0"+seconds;
    let day = time_now.getDay();

    //按格式写入时间
    document.getElementById("times").innerHTML =
        `${year}-${month}-${date}\t${Week[day]}\t${hours}:${minutes}:${seconds}`;
}

//使用定时器每秒向div写入当前时间
setInterval("getDate()", 1000);
