/***************************
#  *  index.js
#  * Version Number	: 1.0
#  * Configuration Identifier: 
#  * Modified by:  Shrilesh Kale and Pushkar Kulkarni       
#  * Modified Date:  12/07/2020       
#  * Description: Javascript code for fronted operations.Handles every frontend query and pass it controller.py code
#  **************************/

/*-----------SLIDER BAR START----------*/
// # *******************************************************************************
//   # Function    : click(function(event)()
//   # Description : Function to emit an event from backend to frontend
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/


// slider 1
var rng1 = document.querySelector("#slide1");

var listener = function() {
	window.requestAnimationFrame(function() {
		document.querySelector("#show1").innerHTML = rng1.value;
	});
};
$('#dimpositive1').click(function(event) {
	 console.log("inside positive");
 	 	$.getJSON('/dimmingpositive-mode', { },
    function(data) { });

	$("#slide1").val(parseInt($("#slide1").val())+20);
	document.querySelector("#show1").innerHTML = rng1.value;
});
 
$('#dimnegative1').click(function(event) {
	//if value < max
	console.log("inside negative");
 	 	$.getJSON('/dimmingnegative-mode', { },
    function(data) { });
	$("#slide1").val(parseInt($("#slide1").val())-20);  
	document.querySelector("#show1").innerHTML = rng1.value;
});
	
// slider 2
var rng2 = document.querySelector("#slide2");

var listener = function() {
	window.requestAnimationFrame(function() {
		document.querySelector("#show2").innerHTML = rng2.value;
	});
};
$('#dimpositive2').click(function() {
	//if value < max
	console.log("inside positive");
 	 	$.getJSON('/dimmingpositive-mode', { },
    function(data) { });
	$("#slide2").val(parseInt($("#slide2").val())+20);
	document.querySelector("#show2").innerHTML = rng2.value;
});
 
$('#dimnegative2').click(function() {
	//if value < max
	console.log("inside negative");
 	 	$.getJSON('/dimmingnegative-mode', { },
    function(data) { });
	$("#slide2").val(parseInt($("#slide2").val())-20);  
	document.querySelector("#show2").innerHTML = rng2.value;
});
	
 
rng2.addEventListener("mousedown", function() {
	listener();
	rng2.addEventListener("mousemove", listener);
});


// slider 3
var rng3 = document.querySelector("#slide3");

var listener = function() {
	window.requestAnimationFrame(function() {
		document.querySelector("#show3").innerHTML = rng3.value;
	});
};
$('#dimpositive3').click(function() {
	//if value < max
	 console.log("inside positive");
 	 	$.getJSON('/dimmingpositive-mode', { },
    function(data) { });
	$("#slide3").val(parseInt($("#slide3").val())+20);
	document.querySelector("#show3").innerHTML = rng3.value;
		// $("#slide1").trigger('change');	
});
 
$('#dimnegative3').click(function() {
	//if value < max
	console.log("inside negative");
 	 	$.getJSON('/dimmingnegative-mode', { },
    function(data) { });
	$("#slide3").val(parseInt($("#slide3").val())-20);  
	document.querySelector("#show3").innerHTML = rng3.value;
});
	
 
rng3.addEventListener("mousedown", function() {
	listener();
	rng3.addEventListener("mousemove", listener);
});


/*-----------SLIDER BAR END-------------*/	


// # *******************************************************************************
//   # Function    : click(function()()
//   # Description : AJAX call for switch on/off lights
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/

// on / off switch btn
$(".switch-btn").click(function(){
	var value = $('#'+this.id+':checked').val();
	var switch_value;
	var light_no = this.id;
	if (value === undefined){
		switch_value = false 
	}else{
		switch_value = true
	} 

	post_body = {
		"status": switch_value,
		"light": light_no
	}

	$.ajax({
			url: '/device/lignting',
			type: 'post',
			data: JSON.stringify(post_body),
			processData: false,
			dataType: 'json',
			success: function(response) {
				
				console.log("Inside Success_1");
				console.log(response);


			},
			failure: function(response) {
				console.log("Inside Failure");
				console.log(response);
				
			},
			error: function(response) {
				console.log("Inside Error");
				console.log(response);
				
			}
		});


});


// # *******************************************************************************
//   # Function    : { $("#panic").click(function (event)
//   # Description : Function to trigger panic-mode route from backend ( for SMS and Email functionality)
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/

// panic mode button
 $(function() 
 	{ $("#panic").click(function (event)

 	 { $.getJSON('/panic-mode', { },
    function(data) { });
     return false; }); });


$(document).ready(function () {
        $('#panic').click(function () {
        	console.log("Inside Button-1");
            $('#myAlert').show('fade');

            setTimeout(function () {
                $('#myAlert').hide('fade');
            }, 2000);
        });

        $('#linkClose').click(function () {
            $('#myAlert').hide('fade');
        });
    });


// # *******************************************************************************
//   # Function    : $(".automatic-btn").click(function()
//   # Description : Function (AJAX) for switch on/off automatic lights
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/

$(".automatic-btn").click(function(){
	var value = $('#'+this.id+':checked').val();
	var switch_value;
	console.log(value)

	if (value === undefined){
		switch_value = false 
	}else{
		switch_value = true
	} 

	post_body = {
		"status": switch_value,
		
	}

	$.ajax({
			url: '/automaticlighting-mode',
			type: 'post',
			data: JSON.stringify(post_body),
			processData: false,
			dataType: 'json',
			success: function(response) {
				
				console.log("Inside Success_Auto");
				console.log(response);


			},
			failure: function(response) {
				console.log("Inside Failure_Auto");
				console.log(response);
				
			},
			error: function(response) {
				console.log("Inside Error_Auto");
				console.log(response);
				
			}
		});


});



$(document).ready(function () {

        $('#automaticlight').click(function () {
        	console.log("Inside Button-2");
            $('#myAlert-1').show('fade');

            setTimeout(function () {
                $('#myAlert-1').hide('fade');
            }, 2000);

        });

        $('#linkClose-1').click(function () {
            $('#myAlert-1').hide('fade');
        });

    });


// # *******************************************************************************
//   # Function    : $(".normal-btn").click(function()
//   # Description : Function (AJAX) for switch on/off normal lights
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/

$(".normal-btn").click(function(){
	var value = $('#'+this.id+':checked').val();
	var switch_value;
	console.log(value)
	console.log("Fuck me ")

	if (value === undefined){
		switch_value = false 
	}else{
		switch_value = true
	} 

	post_body = {
		"status": switch_value,
		
	}


	$.ajax({
			url: '/normalLight-mode',
			type: 'post',
			data: JSON.stringify(post_body),
			processData: false,
			dataType: 'json',
			success: function(response) {
				
				console.log("Inside Success_Normal");
				console.log(response);


			},
			failure: function(response) {
				console.log("Inside Failure_Normal");
				console.log(response);
				
			},
			error: function(response) {
				console.log("Inside Error_Normal");
				console.log(response);
				
			}
		});


});

$(document).ready(function () {

        $('#normallight').click(function () {
        	console.log("Inside Button-3");
            $('#myAlert-2').show('fade');

            setTimeout(function () {
                $('#myAlert-2').hide('fade');
            }, 2000);

        });

        $('#linkClose-2').click(function () {
            $('#myAlert-2').hide('fade');
        });

    });

// # *******************************************************************************
//   # Function    :  $("#stoplight").click(function ()
//   # Description : Function to trigger lightsOff-mode route from backend
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/


 // Stop light
$(function() 
 	{ $("#stoplight").click(function (event)
 	 { $.getJSON('/lightsOff-mode', { },
    function(data) { });
     return false; }); });




$(document).ready(function () {

        $('#stoplight').click(function () {
        	console.log("Inside stop light");
            $('#myAlert-3').show('fade');

            setTimeout(function () {
                $('#myAlert-3').hide('fade');
            }, 2000);

        });

        $('#linkClose-3').click(function () {
            $('#myAlert-3').hide('fade');
        });

    });



// # *******************************************************************************
//   # Function    : $("#energymonitoring").click(function ()
//   # Description : Function to trigger energy-panel route from backend
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/

// Energy monitoring button
$(function() 
 	{ $("#energymonitoring").click(function (event)

 	 { $.getJSON('/energy-Panel', { },
    function(data) { });
 	 console.log("inside energymonitoring")
     return false; }); });


// # *******************************************************************************
//   # Function    : $("#resetbutton").click(function (event)
//   # Description : Function to trigger reset-mode route from backend
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/
// Reset button
$(function() 

 	{ $("#resetbutton").click(function (event)
 	 { $.getJSON('/reset-mode', { },
    function(data) { });
 	 console.log("inside reset")
     return false; }); });

function loadpage(time)
{
	console.log("inside reset-1")
setTimeout("location.reload(true);",time);
} 

// # *******************************************************************************
//   # Function    : showtimedateday(),startTime() ,checkTime(),startDate()
//   # Description : Function to show current date,time and week Day
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/


function showtimedateday()
{
	startTime()
	startDay()
	startDate()
}



function startTime() 
{
	var today = new Date();
	var h = today.getHours();
	var m = today.getMinutes();
	var s = today.getSeconds();
	m = checkTime(m);
	s = checkTime(s);
	document.getElementById('txt').innerHTML =
	h + ":" + m + ":" + s;
	var t = setTimeout(startTime, 500);
}

function checkTime(i) 
{
	if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
	return i;
}

function startDay()
{
	var day;
	switch (new Date().getDay()) 
	{
	  case 0:
	    day = "Sunday";
	    break;
	  case 1:
	    day = "Monday";
	    break;
	  case 2:
	    day = "Tuesday";
	    break;
	  case 3:
	    day = "Wednesday";
	    break;
	  case 4:
	    day = "Thursday";
	    break;
	  case 5:
	    day = "Friday";
	    break;
	  case  6:
	    day = "Saturday";
	}
	document.getElementById("day").innerHTML = day;
						
}

function startDate()
{
	
	n =  new Date();
	y = n.getFullYear();
	m = n.getMonth() + 1;
	d = n.getDate();
	document.getElementById("date").innerHTML = m + "/" + d + "/" + y;
						
}



// # *******************************************************************************
//   # Function    : sDisableAutoNormOFF() ,StopLightOp(),NormLightOp() ,AutoLightOp() 
//   # Description : Functions for buttons event handling (e,g If automatic light button is ON, 
//                   then Normal Light button should be disabled etc)
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/


function DisableAutoNormOFF() 
{
  var ReadToggleSw1 = document.getElementById("1");
  var ReadToggleSw2 = document.getElementById("2");
  var ReadToggleSw3 = document.getElementById("3");
  if (ReadToggleSw1.checked == 1 || ReadToggleSw2.checked == 1 || ReadToggleSw3.checked == 1)
  {
    document.getElementById("swautomaticlight").disabled = true;
    document.getElementById("swnormallight").disabled = true;
    document.getElementById("swstoplight").disabled = true;
  } 
  else 
  {
     document.getElementById("swautomaticlight").disabled = false;
      document.getElementById("swnormallight").disabled = false;
      document.getElementById("swstoplight").disabled = false;
  }
}


function StopLightOp() 
{
	console.log("inside_stoplight")
	document.getElementById("automaticlight").checked = false;
	document.getElementById("normallight").checked = false;
	document.getElementById("automaticlight").disabled = false;
	document.getElementById("normallight").disabled = false;
	document.getElementById("1").disabled = false;
	document.getElementById("2").disabled = false;
	document.getElementById("3").disabled = false;
}

function NormLightOp() 
{
	var ReadToggleSw = document.getElementById("normallight");
	if (ReadToggleSw.checked == 1)
	{
		document.getElementById("automaticlight").checked = false;
		document.getElementById("1").checked = false;
		document.getElementById("2").checked = false;
		document.getElementById("3").checked = false;
		document.getElementById("automaticlight").disabled = true;
		document.getElementById("1").disabled = true;
		document.getElementById("2").disabled = true;
		document.getElementById("3").disabled = true;

	}
	else
	{
		document.getElementById("automaticlight").disabled = false;
		document.getElementById("1").disabled = false;
		document.getElementById("2").disabled = false;
		document.getElementById("3").disabled = false;
	}
    

}


function AutoLightOp() 
{
	console.log("inside autolightop")
	var ReadToggleSw = document.getElementById("automaticlight");
	if (ReadToggleSw.checked == 1)
	{
		console.log("inside autolightop if")
		document.getElementById("normallight").checked = false;
		document.getElementById("1").checked = false;
		document.getElementById("2").checked = false;
		document.getElementById("3").checked = false;
		document.getElementById("normallight").disabled = true;
		document.getElementById("1").disabled = true;
		document.getElementById("2").disabled = true;
		document.getElementById("3").disabled = true;

	}
	else
	{
		console.log("inside autolightop else")
		document.getElementById("normallight").disabled = false;
		document.getElementById("1").disabled = false;
		document.getElementById("2").disabled = false;
		document.getElementById("3").disabled = false;
	}
    

}


// # *******************************************************************************
//   # Function    : getTempHumi()
//   # Description : Function (AJAX) to get temperature and humidity
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/


function getTempHumi(){
	$.ajax({
		url: '/device/environment',
		type: 'GET',
		processData: false,
		dataType: 'json',
		success: function(response) {
			
			console.log("Inside Success");
			console.log("temperature response",response);
			$("#temperature").html(response.temperature);
			$("#humidity").html(response.humidity);
			
		},
		failure: function(response) {
			console.log("Inside Failure");
			console.log(response);
		},
		error: function(response) {
			console.log("Inside Error");
			console.log(response);
		}
	});
};


// # *******************************************************************************
//   # Function    : setInterval()
//   # Description : Function to poll temperature and humidity values using specified timings
//   #               
//   # Input       : NA
//   # Output      : NA
//   # Return      : NA
// # *******************************************************************************/

$(document).ready(function () {
	setInterval(function(){ 
		getTempHumi();
	}, 20000);

});



