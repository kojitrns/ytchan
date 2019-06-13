var playerSet = false
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var ytPlayer = null
var videoIds = []

const playVideo = function() {
  console.log("playVideo")
  const videoId = event.target.id
  var cur = videoIds.findIndex( (id) => {return id===videoId});

  $('body, html').scrollTop(0);
  if(!playerSet){
    playerSet = true
    ytPlayer = new YT.Player(
    'player', // 埋め込む場所の指定
      {
        width: 740, // プレーヤーの幅
        height: 500, // プレーヤーの高さ
        videoId: videoId,
        events: {
          'onReady': onPlayerReady,
          'onStateChange': onPlayerStateChange
        }
      }
    );
  }
  else {
    cur = videoIds.findIndex( (id) => {return id===videoId});
    ytPlayer.loadVideoById(videoId ,0);
  }
  function nextVideoProcess(){

  }
  function onPlayerStateChange(event){
    switch(event.data) {
      case YT.PlayerState.ENDED:
        cur = (cur + 1) % videoIds.length;
        ytPlayer.loadVideoById(videoIds[cur] ,0);
        break;
    }
  }
  function onPlayerReady(event) {
    event.target.playVideo();
  }
  function onError(event) {
    nextVideoProcess();
  }
}