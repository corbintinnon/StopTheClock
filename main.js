// Velo API Reference: https://www.wix.com/velo/reference/api-overview/introduction

	// Call functions on page elements, e.g.:
	// $w("#button1").label = "Click me!";
import wixAnimations from 'wix-animations';
import {fetch} from 'wix-fetch'; 

var imgArray = [$w('#image14'), $w('#image17'), $w('#image15'), $w('#image16'), $w('#image18')];
var fallDist = [70, 210, 70, 80, 100];
var imgFallen = new Array(imgArray.length);
var lastFallen = -1;
const today1 = new Date();
var nowTime = today1.getTime();
var life = 0;
var ind;
var timeFunc;
var backChanged = false;
$w('#donationConfirmed').hide();
$w("#smoke").hide();
$w("#smoke2").hide();

	// Click "Run", or Preview your site, to execute your code
$w.onReady(function () {
	updateBird();
	updateLadyBug();
  updateFox();
  getTreeIndex();
  updateTrees();
  updateTimer();
  updateFacts();
});
function updateTimer () {
  $w('#health').text = "Environment Health: " + String(Math.floor((1-timeFunc)*100)) + "%";
  setTimeout(updateTimer, 500)
}
function chngFirst () {
  $w("#section1").background.src = "https://static.wixstatic.com/media/b9b13c_472f26b53b114eae9a450ef07c87b269~mv2.png";
  $w("#image13").hide("fade");
  $w("#image10").hide("fade");
  $w("#fox").show("fade");
  $w("#image17").src = "https://static.wixstatic.com/media/b9b13c_42e4b03614364d54901697318c11494b~mv2.png";
  //$w("#image1").src = "https://static.wixstatic.com/media/b9b13c_5014b10759bd4ad1a55b9138b3e7a276~mv2.png";
}
function chngBack () {
  $w("#section1").background.src = "https://static.wixstatic.com/media/b9b13c_8dd0b3d3f14149f18a99622a41e2c978~mv2.jpg";
  $w("#image13").show("fade");
  $w("#image10").show("fade");
  $w("#fox").show("fade");
  $w("#image17").src = "https://static.wixstatic.com/media/b9b13c_25d314bfb64b4312b187232ef188c22a~mv2.png";
  //$w("#image1").src = "https://static.wixstatic.com/media/b9b13c_2b38203eae6c4296859b1b8308e74a2b~mv2.gif";
}

function updateTrees () {
  //var ind = getTreeIndex();
if (timeFunc > 0.4 && !backChanged) {
  backChanged = true;
  $w("#smoke").show("fade")
  $w("#fox").hide();
  setTimeout(chngFirst, 4000);
  let timeline = wixAnimations.timeline({
        "repeat": 0
    });
    timeline.add($w("#smoke"), {
      "opacity": 1,
      "duration": 0
    });
    timeline.add($w("#smoke"), {
      //how long it takes to update
      "scale": 2,
      "scaleX": 20,
      "x": 1500,
      "duration": 5000
    });
    timeline.add($w("#smoke"), {
        "opacity": 0,
        "duration": 500
      }, 
      "+=200");
    timeline.add($w("#smoke"), {
      "duration": 10,
      "x": 0
    }, 
    "+=10");
  timeline.play();
}
else if (timeFunc < 0.4 && backChanged) {
  setTimeout(chngBack, 4000);
  backChanged = false;
  $w("#smoke2").show("fade")
  $w("#fox").hide();
  let timeline = wixAnimations.timeline({
        "repeat": 0
    });
    timeline.add($w("#smoke2"), {
      "opacity": 1,
      "duration": 0
    });
    timeline.add($w("#smoke2"), {
      //how long it takes to update
      "scale": 2,
      "scaleX": 20,
      "x": -1500,
      "duration": 5000
    });
    timeline.add($w("#smoke2"), {
        "opacity": 0,
        "duration": 500
      }, 
      "+=200");
    timeline.add($w("#smoke2"), {
      "duration": 10,
      "x": 0
    }, 
    "+=10");
  timeline.play();

}
  
if (!imgFallen[ind] && ind != lastFallen) {
    lastFallen++;
    let timeline = wixAnimations.timeline({
        "repeat": 0
    });
    var img = imgArray[lastFallen];
    timeline.add(imgArray[lastFallen], {
      //how long it takes to update
      "rotate": (lastFallen % 2) ? -90 : 90,
      "rotateDirection": (lastFallen % 2) ? "ccw" : "cw",
      "y": fallDist[lastFallen],
      "x": (lastFallen % 2) ? -100 : 100,
      "duration": 5000,
      "opacity": 1
    });
    timeline.add( 
      imgArray[lastFallen], {
        "opacity": 1,
        "duration": 500
      }, 
      "+=1000");
      timeline.play();
      imgFallen[lastFallen] = 1;
      console.log(lastFallen, ": fallen")
}
else if (ind < lastFallen){
  while (ind < lastFallen){
    console.log(lastFallen, ": risen")
    let timeline = wixAnimations.timeline({
          "repeat": 0
      });
      timeline.add(imgArray[lastFallen], {
        //how long it takes to update
        "rotate": 0,
        "rotateDirection": (lastFallen % 2) ? "cw" : "ccw",
        "y": 0,
        "x": 0,
        "duration": 5000,
        "opacity": 1
      });
      timeline.play();
    imgFallen[lastFallen] = 0;
    lastFallen--;
  }
}
  
  //time for how often the animation updates
  setTimeout(updateTrees, 2000);
}
function getTreeIndex () {
  var newTime = new Date();
  //var timeFunc = Math.floor( (1 + -200000000*(today.getTime()/nowTime - 1) + life)*(imgArray.length-1) );
  timeFunc = 1/(1+Math.exp(100000000*(1-newTime.getTime()/nowTime)+1.8+life));
  ind = Math.floor(timeFunc*(imgArray.length-1));

  setTimeout(getTreeIndex, 500);
}

function updateLadyBug() {
	let timeline = wixAnimations.timeline({
        "repeat": -1,
		"yoyo": false
    });
    timeline.add($w('#image10'), {
        //how long it takes to update
        "duration": 4000,
		"x": "+=700",
		"easing": "linear"
    });
    timeline.play();
}
function updateFox() {
	let timeline = wixAnimations.timeline({
        //"repeat": -1,
		    //"yoyo": true
    });
    timeline.add($w('#fox'), {
        //how long it takes to update
        "duration": 4000,
		"x": "-=300",
		"easing": "easeInOutSine"
    });
    timeline.onComplete(() =>{
      $w('#fox').src = backChanged ?  "https://static.wixstatic.com/media/b9b13c_605383dcc707420b83374491c2a7eb41~mv2.gif":  "https://static.wixstatic.com/media/b9b13c_65058ba380344b5a9fcf31ca0800b52d~mv2.gif";
      timeline.reverse();
    })
    
    timeline.onReverseComplete(() =>{
      $w('#fox').src = backChanged ? "https://static.wixstatic.com/media/b9b13c_635e4d39324a48029cf46c5766c75662~mv2.gif":"https://static.wixstatic.com/media/b9b13c_b437c2d90dbe4ba98af43ba2b788fc20~mv2.gif";
      timeline.play();
    })
    timeline.play();
}

function updateBird() {
  let timeline = wixAnimations.timeline({
        "repeat": -1,
		"yoyo": false
    });
    timeline.add($w('#image2'), {
        //how long it takes to update
        "duration": 0,
		"x": "-=1200"
    });
    timeline.add($w('#image2'), {
        //how long it takes to update
        "duration": 8000,
		"x": "+=3200",
		"easing": "easeInOutQuad"
    });
    timeline.play();
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function button1_click(event) {
  life += 0.5;
  let timeline = wixAnimations.timeline({
        "repeat": 0
  });
  timeline.add($w('#donationConfirmed'), {
      //how long it takes to update
      "duration": 0,
      "opacity": 0
  });
  timeline.add($w('#donationConfirmed'), {
      //how long it takes to update
      "duration": 500,
      "opacity": 1
  });
  timeline.add($w('#donationConfirmed'), {
      //how long it takes to update
      "duration": 5000,
      "y": 1000,
      "opacity": 0,
      "easing": "easeInOutQuad"
  },"+=1000");
  timeline.add($w('#donationConfirmed'), {
      //how long it takes to update
      "duration": 100,
      "y": 0,
      "opacity": 0
  },"+=1000");
  timeline.play();

  //Mastercard confirmation
  console.log("Retrieving information");
    //$w("#result").text = "Retrieving information for " + $w("#currencyInput").value;
    TransactionNotification()
  //imgFallen[ind] = 1;
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
}

const facts = ["The 2022 global Living Planet Index shows an average 69% decrease in relative abundance of monitored wildlife populations between 1970 and 2018.",
                "The global abundance of oceanic sharks and rays has declined by 71% over the last 50 years, due primarily to an 18-fold increase in fishing pressure since 1970.",
                "Humans use as many ecological resources as if we lived on almost two Earths.",
                "Amazonian Indigenous organisations representing 511 nations and allies are calling for a global agreement for the permanent protection of 80% of the Amazon by 2025.",
                "Data shows that 26% of the Amazon is under a state of advanced disturbance 176 which includes forest degradation, recurrent fires, and deforestation",
                "We have already lost 17% of the original extent of the [Amazon] and an additional 17% has been degraded",
                "We need to urgently ramp up mitigation actions to avert a dangerous rise in global temperatures beyond 1.5°C",
                "Unless we limit warming to 1.5°C, climate change is likely to become the dominant cause of biodiversity loss in the coming decades.",
                " Latin America shows the greatest regional decline in average population abundance (94%)."]
function updateFacts() {
  var i = Math.floor(Math.random()*facts.length);
  //$w("#facts").hide("fade");
  $w("#facts").show("fade");
  $w("#facts").text = facts[i];

  setTimeout(updateFacts, 10000)
}
  // Velo API Reference: https://www.wix.com/velo/reference/api-overview/introduction
//import {TransactionNotification} from 'backend/serviceModule.js';


async function TransactionNotification() {
  const url = 'https://cbc-fintech.azurewebsites.net/cards/recent_transactions/fb6adc1c-8139-4b07-97dc-bd752847e842';
  
  return fetch(url, {method: 'post'})
    .then(response => response.json())
}
/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/

