// const channelDataCont = ['maincategory','subcategory','channelid','title','viewcount','videocount','subscribercount',
// 'thumbnail_url','description','keywords','uploads_id', 'publishe_date']


const myappAddr = "api/api.php"
const ytAddr = "https://www.googleapis.com/youtube/v3/"
const apiKey = "AIzaSyD3R2gavNlItHEZWTt-_UOMEwFwMN5reiQ"
const tableMap = {channelData: "channel", videoData: "video"}

var playerSet = false
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var ytPlayer = null

class Mgr extends React.Component {

  constructor(props) {
    super(props)
    this.state = {channelData: [], videoData: [], selectedChannelIds: [], curCategory: "ニュース",
      selectedCategory: "ニュース", selectedSubCategory: "地震", visibleCont: "channels", categoryInputMode: true,
      mainCategoryInputs: [], subCategoryInputs: [], searchResult: [], lastSearchedWord: null, nextToken: null}
    // this. = this..bind(this)
    this.clearSelect = this.clearSelect.bind(this)
    this.onChangeCategorySelector = this.onChangeCategorySelector.bind(this)
    this.onChangeSubCategorySelector = this.onChangeSubCategorySelector.bind(this)
    this.handleKeyPress = this.handleKeyPress.bind(this)
    this.onChangeMode = this.onChangeMode.bind(this)
  }

  processData(allData) {
    var res = []
    if(allData[0]['maincategory']) {
      allData.forEach(data => {
          if(res[data['maincategory']] === undefined)
            res[data['maincategory']] = []
          if(res[data['maincategory']][data['subcategory']] === undefined)
            res[data['maincategory']][data['subcategory']] = []
          res[data['maincategory']][data['subcategory']].push(data)
      })
    }

    if(allData[0]['main_category']) {
      allData.forEach(data => {
          if(res[data['main_category']] === undefined)
            res[data['main_category']] = []
          if(res[data['main_category']][data['sub_category']] === undefined)
            res[data['main_category']][data['sub_category']] = []
          res[data['main_category']][data['sub_category']].push(data)
      })
    }
    return res
  }

  fetchData(dataName) {
    fetch(myappAddr, {
      method: 'POST',
      body: JSON.stringify({opType: "fetch", table: tableMap[dataName]})
    })
      .then(res => res.json())
      .then(json => {
        this.setState({[dataName]: this.processData(json)})
    })
  }

  callApi = (data) => {
    fetch(myappAddr, {
      method: 'POST', // or 'PUT'
      body: JSON.stringify(data),
      headers:{
        'Content-Type': 'application/json'
      }
    })
  }

  deleteChannel = () => {
    this.state.selectedChannelIds.forEach(channelId =>
    {
      const sendData = {
          opType: 'delete',
          channelid: channelId
      }
      this.callApi(sendData)
    })
    this.clearSelect()
  }

  moveChannel = () => {
    const sendData = {
          opType: 'move',
          maincategory: this.state.selectedCategory,
          subcategory: this.state.selectedSubCategory
    }
    this.state.selectedChannelIds.forEach(channelId =>
    {
      sendData.channelid = channelId
      this.callApi(sendData)
    })
    this.clearSelect()
  }

  fetchYTLapper = (reqKind, params, clb) => {
    fetch(ytAddr + reqKind +'?' + params.toString()).then(res => res.json()).then(json => {
      clb(json)
    })
  }

  addChannel = (channelId) => {
    const clb = (chanData) => {
      if(chanData.items)
        chanData = chanData.items[0]
      const sendData = {
            opType: 'add',
            maincategory: this.state.selectedCategory,
            subcategory: this.state.selectedSubCategory,
      }
      sendData.channelid = chanData.id,
      sendData.title = chanData.snippet.title
      sendData.viewcount = chanData.statistics.viewCount
      sendData.videocount = chanData.statistics.videoCount
      sendData.subscribercount = chanData.statistics.subscriberCount
      sendData.thumbnail_url = chanData.snippet.thumbnails.default.url
      sendData.description = chanData.snippet.description
      sendData.keywords = chanData.brandingSettings.channel.keywords
      sendData.uploads_id = chanData.contentDetails.relatedPlaylists.uploads
      sendData.publish_date = chanData.snippet.publishedAt
      this.callApi(sendData)
    }
    if(this.state.visibleCont === 'searchResult') {
      this.state.searchResult.forEach(chanData => {
        if(this.state.selectedChannelIds.includes(chanData.id))
          clb(chanData);
      })
      this.clearSelect()
    }
    else {
      this.getChannelData(channelId, clb)
    }
  }

  getChannelData = (channelId, clb) => {
    const params = new URLSearchParams();
    params.set('key', apiKey)
    params.set('part',  'statistics,snippet,brandingSettings,contentDetails')
    params.set('id', channelId)
    this.fetchYTLapper('channels', params, clb)
  }

  searchChannel = (word, isNewSearch) => {
    const params = new URLSearchParams();
    params.set('key', apiKey)
    params.set('part', 'snippet')
    params.set('maxResults', 50)
    params.set('order', 'viewCount')
    params.set('type', 'channel')
    params.set('q', word)
    params.set('regionCode', 'JP')

    let completedNum = 0;
    let curChannelResult = this.state.searchResult
    if(isNewSearch) {
      curChannelResult = []
      this.setState({nextToken: null})
    }
    else if(this.state.nextToken)
      params.set('pageToken', this.state.nextToken)

    const getChanClb = (json) => {
      const chanData = json.items[0]
      if(chanData) curChannelResult.push(chanData)
      completedNum++
    }

    const mainClb = (json) => {
      this.setState({nextToken: json.nextPageToken})
      const finIds = []
      json.items.forEach(channel => {
        if(!finIds.includes(channel.id.channelId)){
          finIds.push(channel.id.channelId)
          this.getChannelData(channel.id.channelId, getChanClb)
        }
        else
          completedNum++
      })
      const countup = () => {
        if(json.items.length === completedNum)
          this.setState({searchResult: curChannelResult})
        else
          setTimeout(countup, 100);
      }
      countup();
    }
    this.fetchYTLapper('search', params, mainClb)
  }

  searchMore = () => {
    if(this.state.nextToken)
      this.searchChannel(this.state.lastSearchedWord, false)
  }

  selecteChannel(channelId){
    const curList = this.state.selectedChannelIds
    if(curList.includes(channelId)) {
      this.setState({selectedChannelIds: curList.filter(id => id!==channelId)})
      return
    }
    curList.push(channelId)
    this.setState({selectedChannelIds: curList})
  }

  selecteChannelOfSubcategory(subCategory) {
    const channels = this.state.channelData
    const curList = this.state.selectedChannelIds
    const subcategoryArray = this.state.channelData[this.state.curCategory][subCategory]
    subcategoryArray.forEach(channel => {
      curList.push(channel['channelid'])
    })
    this.setState({selectedChannelIds: curList})
  }

  clearSelect() {
    this.setState({selectedChannelIds: []})
  }

  changeCategory = (category) => {
    this.setState({curCategory: category})
  }

  handleKeyPress(event) {
    if(event.key == 'Enter') {
      switch(event.target.name) {
        case "channelId":
          this.addChannel(event.target.value)
          break
        case "category":
          const curMainList = this.state.mainCategoryInputs
          this.setState({mainCategoryInputs: curMainList.concat(event.target.value)})
          break
        case "subCategory":
          const curSubList = this.state.subCategoryInputs
          this.setState({subCategoryInputs: curSubList.concat(event.target.value)})
          break
        case "search":
          this.searchChannel(event.target.value, true)
          this.setState({lastSearchedWord: event.target.value})
          this.setState({visibleCont: "searchResult" })
          break
      }
    }
  }

  onChangeCategorySelector(event) {
    this.setState({selectedCategory: event.target.value})
    var subcategory = Object.keys(this.state.channelData[event.target.value])[0]
    this.setState({selectedSubCategory: subcategory})
  }

  onChangeSubCategorySelector(event) {
    this.setState({selectedSubCategory: event.target.value})
  }

  onChangeMode(mode) {
    const currentCont = this.state.visibleCont
    let nextCont = null
    if(mode === 'search') nextCont = 'searchResult'
    else {
      switch(currentCont) {
        case "channels":
          nextCont = "videos"
          break
        case "videos":
          nextCont = "channels"
          break
        default :
          nextCont = "channels"
      }
    }
    this.setState({visibleCont: nextCont})

    if(this.state.videoData.length === 0)
      this.fetchData("videoData")
  }

  getSearchCont() {
    const searchCont = []
    this.state.searchResult.forEach(channel => {
      searchCont.push(
          <div className="chan-box">
            <img src = {channel.snippet.thumbnails.medium.url} />
            <div className="chan-info-box" onClick={this.selecteChannel.bind(this, channel.id)}>
              <div className="counter-box">
                <p>{channel.statistics.viewCount}</p>
                <p>{channel.statistics.videoCount}</p>
                <p>{channel.statistics.subscriberCount}</p>
              </div>
              <div className="detail-box">
                <img id="desc-img" src="https://img.icons8.com/ios/50/000000/questions.png" />
                <p>{channel.snippet.description}</p>
                <a href={"https://socialblade.com/youtube/channel/" + channel.id} target="_blank" title="socialblade">
                <img id="sb-img" src ="../img/sb.png"/>
                </a>
              </div>
            </div>
            <div className = {this.state.selectedChannelIds.includes(channel.id) ? "selected-title-box":"chan-title-box"}>
              <a href={"https://www.youtube.com/channel/" + channel.id} target="_blank" title={channel.snippet.title}>{channel.snippet.title}</a>
            </div>
          </div>
      )
    })
    searchCont.push(<div className="chan-box" onClick={this.searchMore}><h2>more</h2></div>)
    return searchCont
  }

  playVideo(event) {
    console.log("playVideo")
    const videoId = event.target.id

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
      ytPlayer.loadVideoById(videoId ,0);
    }
    function nextVideoProcess(){
    }
    function onPlayerStateChange(event){
      switch(event.data) {
        case YT.PlayerState.ENDED:
          // nextVideoProcess();
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

  componentDidMount() {
    console.log("componentDidMount")
    this.fetchData("channelData")
  }

  render(){
    console.log("render")
    const categoryCont = []
    const categorySelectorCont = []
    const subCategorySelectorCont = []
    const leftPanelCont = []
    const mainCont = [<h2>{this.state.curCategory}</h2>]
    let dataName = 'channelData'

    Object.keys(this.state.channelData).forEach(category => {
      categoryCont.push(<span onClick={this.changeCategory.bind(this, category)}>{category} </span>)
      categorySelectorCont.push(<option value={category} >{category}</option>)
    })
    this.state.mainCategoryInputs.forEach(category => {
      categorySelectorCont.push(<option value={category}>{category}</option>)
    })

    if(this.state.channelData[this.state.selectedCategory]){
      subcategoryList = Object.keys(this.state.channelData[this.state.selectedCategory])
      subcategoryList.forEach(subcategory => {
        subCategorySelectorCont.push(<option value={subcategory}>{subcategory}</option>)
      })
    }
    this.state.subCategoryInputs.forEach(subcategory => {
      subCategorySelectorCont.push(<option value={subcategory} >{subcategory}</option>)
    })

    var subcategoryList = []
    if(this.state.channelData[this.state.curCategory]){
      subcategoryList = Object.keys(this.state.channelData[this.state.curCategory])
    }


    if(this.state.visibleCont === "channels") {
      const channelPanel = []
      subcategoryList.forEach(subcategory => {
        const subcategoryArray = this.state.channelData[this.state.curCategory][subcategory]
        const channelTable = []
        channelTable.push(<h3 id={subcategory} onClick={this.selecteChannelOfSubcategory.bind(this, subcategory)}>
          ■{subcategory}</h3>)
        leftPanelCont.push(<p><a href={"#"+subcategory}>{subcategory}</a></p>)
        subcategoryArray.sort(function(a,b){
          if(a.viewcount < b.viewcount) return 1;
          if(a.viewcount > b.viewcount) return -1;
          return 0;
        })

        subcategoryArray.forEach(data => {
          channelTable.push(
            <div className="chan-box">
              <img src = {data['thumbnailurl']} />
              <div className="chan-info-box" onClick={this.selecteChannel.bind(this, data['channelid'])}>
                <div className="counter-box">
                  <p>{data['viewcount']}</p><p>{data['videocount']}</p><p>{data['subscribercount']}</p>
                </div>
                <div className="detail-box">
                  <img id="desc-img" src="https://img.icons8.com/ios/50/000000/questions.png" />
                  <p>{data['description']}</p>
                  <a href={"https://socialblade.com/youtube/channel/" + data['channelid']} target="_blank" title="socialblade">
                  <img id="sb-img" src ="../img/sb.png"/>
                  </a>
                </div>
              </div>
              <div className = {this.state.selectedChannelIds.includes(data['channelid']) ? "selected-title-box":"chan-title-box"}>
                <a href={"https://www.youtube.com/channel/" + data['channelid']} target="_blank" title={data['channeltitle']}>{data['channeltitle']}</a>
              </div>
            </div>
          )}
        )
        channelPanel.push(<div className="chan-container clearfix">{channelTable}</div>)
      })
      mainCont.push(channelPanel)
    }
    else if(this.state.visibleCont === "videos"){
      dataName = 'videoData'
      const videoCont = []
      if(this.state.videoData[this.state.curCategory])
      subcategoryList.forEach(subcategory => {
        const videos = this.state.videoData[this.state.curCategory][subcategory]
        if(videos === undefined) return
        const videoSubCont = []
        videoSubCont.push(<h3 id={subcategory}>■{subcategory}</h3>)
        leftPanelCont.push(<p><a href={"#"+subcategory}>{subcategory}</a></p>)

        videos.sort(function(a,b){
          if(a.published_at < b.published_at) return 1;
          if(a.published_at > b.published_at) return -1;
          return 0;
        })
        videos.forEach(data => {
            videoSubCont.push(
              <div className="video-box">
                <a href={"https://www.youtube.com/watch?v=" + data['video_id']} target="_blank">
                <img src = {data['thumbnail']} />
                <p>{data['video_title']}</p></a>
                <a href={"https://www.youtube.com/channel/" + data['channel_id']} target="_blank" title={data['channel_title']}>
                <p>{data['channel_title']}</p></a>
                <span> {data['view_count']+ " views  "}</span> <span>{data['published_at'].split("T")[0]}</span>
                <span onClick={this.playVideo} id={data['video_id']}> play</span>
              </div>)
        })
        videoCont.push(<div className="clearfix">{videoSubCont}</div>)
      })
      mainCont.push(<div><h3>新着動画</h3>{videoCont}</div>)
    }
    else {
      mainCont.push(this.getSearchCont())
    }

    return (
      <div>
        <header className="site-header"><nav><b>カテゴリ:</b>{categoryCont}</nav></header>
        <div className="header-emb"></div>
        <div className="left-panel">{leftPanelCont}</div>
        <div className="main-category-panel">
        <center><p><div id="player"></div></p></center>
          <p><label onClick={this.onChangeMode.bind(this, "search")}>検索:</label><input type="text" name="search" onKeyPress={this.handleKeyPress} /></p>
          {mainCont}
        </div>
        <div className="controlPanel">
          <center>
            <div className="mode-selector">
              <span onClick={this.onChangeMode}>チャンネル/動画</span>
            </div>
            <button onClick={this.deleteChannel}>Delete</button>
            <button onClick={this.fetchData.bind(this, dataName)}>Update</button>
            <p><select size="10" name="mainCategory" value={this.state.selectedCategory} onChange={this.onChangeCategorySelector}>{categorySelectorCont}</select></p>
            <p><select size="10" name="subCategory" value={this.state.selectedSubCategory}
            onChange={this.onChangeSubCategorySelector}>{subCategorySelectorCont}</select></p>
            <button onClick={this.addChannel}>Add</button>
            <button onClick={this.moveChannel}>Move</button>
            <button onClick={this.clearSelect}>Clear</button>
            <div className="inputs">
              <p><label>main:</label><input type="text" name="category" onKeyPress={this.handleKeyPress} /></p>
              <p><label>sub:</label><input type="text" name="subCategory" onKeyPress={this.handleKeyPress} /></p>
              <p><label>id:</label><input type="text" name="channelId" onKeyPress={this.handleKeyPress} /></p>
            </div>
          </center>
        </div>
      </div>
    );
  }
};

ReactDOM.render(
  <Mgr />,
  document.getElementById('chanManager')
);