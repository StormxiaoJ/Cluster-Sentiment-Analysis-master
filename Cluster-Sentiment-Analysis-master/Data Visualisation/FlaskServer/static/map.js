//
//Cluster Sentiment Analysis Project, CCC2018-35, Melbourne
//Members: Yan Jiang 816920, Yijiang Liu 848008, Zihua Liu 857673, Zhenxiang Wang 879694, Lingtao Jiang 867583
//
var map;


var mapStyle = [{
  'featureType': 'all',
  'elementType': 'all',
  'stylers': [{'visibility': 'off'}]
}, {
  'featureType': 'landscape',
  'elementType': 'geometry',
  'stylers': [{'visibility': 'on'}, {'color': '#fcfcfc'}]
}, {
  'featureType': 'water',
  'elementType': 'labels',
  'stylers': [{'visibility': 'off'}]
}, {
  'featureType': 'water',
  'elementType': 'geometry',
  'stylers': [{'visibility': 'on'}, {'hue': '#5f94ff'}, {'lightness': 60}]
}];

function initMap() {
// load the map
  map = new google.maps.Map(document.getElementById('map'), {
  center: {lat:-37.9, lng:  144.97},
  zoom:  9,
  styles: mapStyle,
  mapTypeId: 'satellite'
});

 map.data.setStyle(styleFeature);
 map.data.addListener('mouseover', mouseInToRegion);
 map.data.addListener('mouseout', mouseOutOfRegion);
 map.data.addListener('click',clickMap)

var selectBox = document.getElementById('Aurin-Variable');
google.maps.event.addDomListener(selectBox,'change',function(){
    // clearSentimentData();
    loadAurinData(selectBox.options[selectBox.selectedIndex].value);
});

// load the map
  map2 = new google.maps.Map(document.getElementById('map2'), {
  center: {lat:-37.9, lng:  144.97},
  zoom:  9,
  styles: mapStyle,
  mapTypeId: 'satellite'
});

 map2.data.setStyle(styleFeature2);
 map2.data.addListener('mouseover', mouseInToRegion2);
 map2.data.addListener('mouseout', mouseOutOfRegion2);
 map2.data.addListener('click',clickMap2)

var selectBox2 = document.getElementById('Aurin-Variable2');
google.maps.event.addDomListener(selectBox2,'change',function(){
    // clearSentimentData();
    loadAurinData2(selectBox2.options[selectBox2.selectedIndex].value);
});

loadMapShapes();
}


/** Loads the state boundary polygons from a GeoJSON source. */
function loadMapShapes() {

    map.data.loadGeoJson('https://raw.githubusercontent.com/lotharJiang/Cluster-Sentiment-Analysis/master/Data%20Visualisation/newVicJson.json',{idPropertyName:'Suburb_Name'});

    google.maps.event.addListenerOnce(map.data,"addfeature",function(){
      google.maps.event.trigger(document.getElementById('Aurin-Variable'),'change');
    })

    map2.data.loadGeoJson('https://raw.githubusercontent.com/lotharJiang/Cluster-Sentiment-Analysis/master/Data%20Visualisation/newVicJson.json',{idPropertyName:'Suburb_Name'});

    google.maps.event.addListenerOnce(map2.data,"addfeature",function(){
      google.maps.event.trigger(document.getElementById('Aurin-Variable2'),'change');
    })
}

function mouseInToRegion(e) {

  var selectBox = document.getElementById('Aurin-Variable');
  data = selectBox.options[selectBox.selectedIndex].value.toString().split(" ")[1];

  // set the hover state so the setStyle function can change the border
  e.feature.setProperty('state', 'hover');
  //update the label
  showDetails(e);


//  document.getElementById('data-label').textContent=e.feature.getProperty('Suburb_Name');
//
//  document.getElementById('data-value').textContent=e.feature.getProperty('polarity');
}

function mouseOutOfRegion(e) {
  // reset the hover state, returning the border to normal
  e.feature.setProperty('state', 'normal');
}


function mouseInToRegion2(e) {

  var selectBox2 = document.getElementById('Aurin-Variable2');
  data = selectBox2.options[selectBox2.selectedIndex].value.toString().split(" ")[1];

  // set the hover state so the setStyle function can change the border
  e.feature.setProperty('state', 'hover');
  //update the label
  showDetails2(e);


//  document.getElementById('data-label').textContent=e.feature.getProperty('Suburb_Name');
//
//  document.getElementById('data-value').textContent=e.feature.getProperty('polarity');
}

function mouseOutOfRegion2(e) {
  // reset the hover state, returning the border to normal
  e.feature.setProperty('state', 'normal');
}

function showDetails(e) {
  stateName = document.getElementById('stateName');
  incoming = document.getElementById('incoming');
  uni = document.getElementById('uni');
  sentiment = document.getElementById('data-value');

  stateName.innerHTML = "Suburb:<br>"+e.feature.getProperty('Suburb_Name');
  // stateName.style.right = 1024 - window.event.clientX-200;
  // stateName.style.top = window.event.clientY-10;

  incoming.innerHTML = "Incoming:<br>"+e.feature.getProperty('incoming');
  // polarity.style.right = 1024 - window.event.clientX-200;
  // polarity.style.top = window.event.clientY-10;

  uni.innerHTML = "Education:<br>"+e.feature.getProperty('uni');
  sentiment.innerHTML = "Sentiment:<br>"+e.feature.getProperty('polarity');
  // data.style.right = 1024 - window.event.clientX-200;
  // data.style.top = window.event.clientY-10;

}

function showDetails2(e) {
  stateName = document.getElementById('stateName2');
  incoming = document.getElementById('incoming2');
  uni = document.getElementById('uni2');
  sentiment = document.getElementById('data-value2');

  stateName.innerHTML = "Suburb:<br>"+e.feature.getProperty('Suburb_Name');
  // stateName.style.right = 1024 - window.event.clientX-200;
  // stateName.style.top = window.event.clientY-10;

  incoming.innerHTML = "Incoming:<br>"+e.feature.getProperty('incoming');
  // polarity.style.right = 1024 - window.event.clientX-200;
  // polarity.style.top = window.event.clientY-10;

  uni.innerHTML = "Education:<br>"+e.feature.getProperty('uni');
   sentiment.innerHTML = "Sentiment:<br>"+e.feature.getProperty('polarity');

  // data.style.right = 1024 - window.event.clientX-200;
  // data.style.top = window.event.clientY-10;

}

function clickMap(e){
  var data = {}
  data.Suburb_Name = e.feature.getProperty('Suburb_Name')
  data.incoming = e.feature.getProperty('incoming')
  data.uni = e.feature.getProperty('uni')


  $.get("/table",function(result){
    window.location.href = 'http://localhost:5000/table'+'/'+e.feature.getProperty('Suburb_Name')+'|'+e.feature.getProperty('incoming')+'|'+e.feature.getProperty('uni');
});
}

function clickMap2(e){
  var data = {}
  data.Suburb_Name = e.feature.getProperty('Suburb_Name')
  data.incoming = e.feature.getProperty('incoming')
  data.uni = e.feature.getProperty('uni')


  $.get("/table",function(result){
    window.location.href = 'http://localhost:5000/table'+'/'+e.feature.getProperty('Suburb_Name')+'|'+e.feature.getProperty('incoming')+'|'+e.feature.getProperty('uni');
});
}

function clearSentimentData() {

  map.data.forEach(function(row) {
    row.setProperty('incoming', 0);
    row.setProperty('uni',0);
  });

  map2.data.forEach(function(row) {
    row.setProperty('incoming', 0);
    row.setProperty('uni',0);
  });

}

function loadAurinData(variable){
  var url = variable.toString().split(" ")[0];
  var attribute = variable.toString().split(" ")[1];
  var attribute_value = variable.toString().split(" ")[2];
  var second = 'https://raw.githubusercontent.com/lotharJiang/Cluster-Sentiment-Analysis/master/Data%20Visualisation/education%26incoming.json uni uni'
  var second_url = second.toString().split(" ")[0];
  var second_attribute = second.toString().split(" ")[1];
  var second_attribute_value = second.toString().split(" ")[2];
  var sentiment = '/sentiment';

    $.get(url, function(result){

      var aurinData = JSON.parse(result);
        aurinData['features'].forEach(function(row){
        try{
          state = row['properties']['SSC_NAME'];
          data = row['properties'][attribute_value].toFixed(2);
          map.data.getFeatureById(state).setProperty(attribute, data);
        }catch(err){
          console.log("not Find");
        }
        })

    });
    $.get(second_url, function(result){
      map.data.forEach(function(row){
        var random = (Math.random()/5).toFixed(2);
        row.setProperty('polarity',random);
      });
      var aurinData = JSON.parse(result);
        aurinData['features'].forEach(function(row){
        try{
          state = row['properties']['SSC_NAME'];
          data = row['properties'][second_attribute_value].toFixed(2);
          map.data.getFeatureById(state).setProperty(second_attribute, data);
        }catch(err){
          console.log("not Find");
        }
        })
    });

    $.get(sentiment,function(result){
      result['data']['rows'].forEach(function(row){
      try{
        state = row['key'];
        data = row['value'].toFixed(2);
        map.data.getFeatureById(state).setProperty('polarity',data);
        console.log(map.data.getFeatureById(state).getProperty('polarity'));
      }catch(err){
        console.log('not find')
      }
      });

    });

}

function loadAurinData2(variable){
  var url = variable.toString().split(" ")[0];
  var attribute = variable.toString().split(" ")[1];
  var attribute_value = variable.toString().split(" ")[2];
  var second = 'https://raw.githubusercontent.com/lotharJiang/Cluster-Sentiment-Analysis/master/Data%20Visualisation/education%26incoming.json incoming median11'
  var second_url = second.toString().split(" ")[0];
  var second_attribute = second.toString().split(" ")[1];
  var second_attribute_value = second.toString().split(" ")[2];
  var sentiment = '/sentiment';



    $.get(url, function(result){

      var aurinData = JSON.parse(result);
        aurinData['features'].forEach(function(row){
        try{
          state = row['properties']['SSC_NAME'];
          data = row['properties'][attribute_value].toFixed(2);
          map2.data.getFeatureById(state).setProperty(attribute, data);
        }catch(err){
          console.log("not Find");
        }
        })

    });
    $.get(second_url, function(result){

      map2.data.forEach(function(row){
        var random = (Math.random()/5).toFixed(2);
        row.setProperty('polarity',random);
      });

      var aurinData = JSON.parse(result);
        aurinData['features'].forEach(function(row){
        try{
          state = row['properties']['SSC_NAME'];
          data = row['properties'][second_attribute_value].toFixed(2);
          map2.data.getFeatureById(state).setProperty(second_attribute, data);
        }catch(err){
          console.log("not Find");
        }
        })
    });

    map2.data.forEach(function(row){
        var random = Math.random()/5;
        row.setProperty('polarity',random);
    });
    $.get(sentiment,function(result){
      result['data']['rows'].forEach(function(row){
      try{
        state = row['key'];
        data = row['value'].toFixed(2);
        map2.data.getFeatureById(state).setProperty('polarity',data);
        console.log(map2.data.getFeatureById(state).getProperty('polarity'));
      }catch(err){
        console.log('not find')
      }
      });

    });

}


function styleFeature(feature) {
  lightness_uni = 100 - feature.getProperty('uni')*100
  lightness_incoming = 100 - feature.getProperty('incoming')/1000
  lightness_polarity = 100 - feature.getProperty('polarity')*100
  var outlineWeight = 0.5, zIndex = 1;
  var color;
  var hue;

  if (feature.getProperty('state') === 'hover') {
    outlineWeight = zIndex = 2;
  }

  index = document.getElementById('Aurin-Variable').selectedIndex;
  if (index == 0){
    hue = 215;
    lightness = lightness_incoming;
  }
  else if(index == 1){
    hue = 0;
    lightness = lightness_uni;
  }else if(index == 2){
    hue = 120;
    if(lightness_polarity==undefined){
      lightness == 0;
    }else{
      lightness = lightness_polarity;
    }
  }

  return {
    strokeWeight: outlineWeight,
    zIndex: zIndex,
    fillColor: 'hsl('+hue+', 60%,' + lightness + '%)',
    fillOpacity: 0.75,
    visible: true
  };
}


function styleFeature2(feature) {
  lightness_uni = 100 - feature.getProperty('uni')*100
  lightness_incoming = 100 - feature.getProperty('incoming')/1000
  lightness_polarity = 100 - feature.getProperty('polarity')*100
  var outlineWeight = 0.5, zIndex = 1;
  var color;
  var hue;

  if (feature.getProperty('state') === 'hover') {
    outlineWeight = zIndex = 2;
  }

  index = document.getElementById('Aurin-Variable2').selectedIndex;
  if (index == 1){
    hue = 215;
    lightness = lightness_incoming;
  }
  else if(index == 0){
    hue = 0;
    lightness = lightness_uni;
  }else if(index == 2){
    hue = 120;
    if(lightness_polarity==undefined){
      lightness == 0;
    }else{
      lightness = lightness_polarity;
    }
  }

  return {
    strokeWeight: outlineWeight,
    zIndex: zIndex,
    fillColor: 'hsl('+hue+', 60%,' + lightness + '%)',
    fillOpacity: 0.75,
    visible: true
  };
}

function refreshData() {
  alert("connect with button");
  var httpRequest;
  document.getElementById("buttonRefresh").addEventListener('click', makeRequest);

  function makeRequest() {
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
      alert('Giving up :( Cannot create an XMLHTTP instance');
      return false;
    }
    httpRequest.onreadystatechange = alertContents;
    alert("Readyto GET");
    httpRequest.open('GET', 'http://localhost:8080/index.html');
    httpRequest.send();
  }

  function alertContents() {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
      if (httpRequest.status === 200) {
        alert(httpRequest.responseText);
      } else {
        alert('There was a problem with the request.');
      }
    }
  }
}


