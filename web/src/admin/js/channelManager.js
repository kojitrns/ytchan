// const channelDataCont = ['maincategory','subcategory','channelid','title','viewcount','videocount','subscribercount',
// 'thumbnail_url','description','keywords','uploads_id', 'publishe_date']

const myappAddr = "api/api.php"
const ytAddr = "https://www.googleapis.com/youtube/v3/channels?"
const apiKey = "AIzaSyD3R2gavNlItHEZWTt-_UOMEwFwMN5reiQ"
const tableMap = {channelData: "channel", videoData: "video"}

class Mgr extends React.Component {

  constructor(props) {
    super(props)
    this.state = {channelData: [], videoData: [], selectedChannelIds: [], curCategory: "ニュース",
      selectedCategory: "ニュース", selectedSubCategory: "地震", modeFlag: true}
    // this. = this..bind(this)
    this.clearSelect = this.clearSelect.bind(this)
    this.onChangeCategorySelector = this.onChangeCategorySelector.bind(this)
    this.onChangeSubCategorySelector = this.onChangeSubCategorySelector.bind(this)
    this.handleKeyPress = this.handleKeyPress.bind(this)
    this.onChangeMode = this.onChangeMode.bind(this)
  }

  processData(allData) {
    var res = []

    if(allData[0]['maincategory'])
    allData.forEach(data => {
        if(res[data['maincategory']]==null)
          res[data['maincategory']]=[]
        if(res[data['maincategory']][data['subcategory']]==null)
          res[data['maincategory']][data['subcategory']]=[]
        res[data['maincategory']][data['subcategory']].push(data)
    })

    if(allData[0]['main_category'])
    allData.forEach(data => {
        if(res[data['main_category']]==null)
          res[data['main_category']]=[]
        if(res[data['main_category']][data['sub_category']]==null)
          res[data['main_category']][data['sub_category']]=[]
        res[data['main_category']][data['sub_category']].push(data)
    })
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

  // function callApi(data){
  callApi = (data) => {
    console.log("callApi",data)
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

  addChannel = (channelId) => {
    const params = new URLSearchParams();
    const sendData = {
          opType: 'add',
          maincategory: this.state.selectedCategory,
          subcategory: this.state.selectedSubCategory,
          channelid: channelId,
    }    

    params.set('key', apiKey)
    params.set('part',  'statistics,snippet,brandingSettings,contentDetails')
    params.set('id', channelId)
    fetch(ytAddr+params.toString()).then(res => res.json()).then(json => {
        var chanData = json.items[0]
        sendData.title = chanData.snippet.title
        sendData.viewcount = chanData.statistics.viewCount
        sendData.videocount = chanData.statistics.videoCount
        sendData.subscribercount = chanData.statistics.subscriberCount
        sendData.thumbnail_url = chanData.snippet.thumbnails.default.url
        sendData.description = chanData.snippet.description
        sendData.keywords = chanData.brandingSettings.channel.keywords
        sendData.uploads_id = chanData.contentDetails.relatedPlaylists.uploads
        sendData.publish_date = chanData.snippet.publishedAt
        // console.log(json,sendData)
        this.callApi(sendData)
      }
    )
  }  

  componentDidMount() {
    console.log("componentDidMount")
    this.fetchData("channelData")
  }

  selecteChannel(channelId){
    const curList = this.state.selectedChannelIds
    this.setState({selectedChannelIds: curList.concat(channelId)})
  }

  clearSelect() {
    this.setState({selectedChannelIds: []})
  }

  changeCategory = (category) => {
    console.log("changeCategory", this)
    this.setState({curCategory: category})
  }

  handleKeyPress(event) {
    if(event.key == 'Enter') {
      console.log("enter",event.target.value)
      this.addChannel(event.target.value)
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

  onChangeMode(event) {
    const currentModeFlag = this.state.modeFlag
    this.setState({modeFlag: !currentModeFlag})
    if(this.state.videoData.length === 0)
      this.fetchData("videoData")
  }


  render(){

    const categoryCont = []
    const categorySelectorCont = []
    const subCategorySelectorCont = []
    const leftPanelCont = []

    Object.keys(this.state.channelData).forEach(category => {
      categoryCont.push(<span onClick={this.changeCategory.bind(this, category)}>{category} </span>)
      categorySelectorCont.push(<option value={category} >{category}</option>)
    })

    if(this.state.channelData[this.state.selectedCategory]){
      subcategoryList = Object.keys(this.state.channelData[this.state.selectedCategory])
      subcategoryList.forEach(subcategory => {
        subCategorySelectorCont.push(<option value={subcategory} >{subcategory}</option>)        
      })
    }

    var subcategoryList = []
    if(this.state.channelData[this.state.curCategory]){
      subcategoryList = Object.keys(this.state.channelData[this.state.curCategory])
    }

    const channelPanel = []

    subcategoryList.forEach(subcategory => {
      const subcategoryArray = this.state.channelData[this.state.curCategory][subcategory]
      const channelTable = []
      channelTable.push(<h3 id={subcategory}>■{subcategory}</h3>)
      leftPanelCont.push(<p><a href={"#"+subcategory}>{subcategory}</a></p>)
      subcategoryArray.sort(function(a,b){
        if(a.viewcount < b.viewcount) return 1;
        if(a.viewcount > b.viewcount) return -1;
        return 0;
      })

      subcategoryArray.forEach(data => {
        channelTable.push(
          <div className="chan-box" onClick={this.selecteChannel.bind(this, data['channelid'])}>
            <img src = {data['thumbnailurl']} />
            <div className="chan-info-box">
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

    const videoCont = []
    if(this.state.videoData[this.state.curCategory])
    subcategoryList.forEach(subcategory => {
      const subcategoryArray = this.state.channelData[this.state.curCategory][subcategory]
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
            </div>)
      })
      videoCont.push(<div className="clearfix">{videoSubCont}</div>)
    })

    const displayCont = this.state.modeFlag ? channelPanel : <div><h3>新着動画</h3>{videoCont}</div>

    return (
      <div>
        <header className="site-header"><nav><b>カテゴリ:</b>{categoryCont}</nav></header><div className="header-emb"></div>
        <div className="left-panel">{leftPanelCont}</div>
        <div className="main-category-panel">
          <h2>{this.state.curCategory}</h2>
          <input type="radio" value="channel" checked={this.state.modeFlag} onChange={this.onChangeMode}/>
          <label>チャンネル</label>
          <input type="radio" value="video"  checked={!this.state.modeFlag} onChange={this.onChangeMode}/>
          <label>動画</label>
          {displayCont}
        </div>
        <div className="controlPanel">
          <center>
            <button onClick={this.deleteChannel}>Delete</button>
            <button onClick={this.fetchData.bind(this,("channelData"))}>Update</button>
            <p><select name="mainCategory" value={this.state.selectedCategory} onChange={this.onChangeCategorySelector}>{categorySelectorCont}</select></p>
            <p><select name="subCategory" value={this.state.selectedSubCategory}
            onChange={this.onChangeSubCategorySelector}>{subCategorySelectorCont}</select></p>
            <button onClick={this.moveChannel}>Move</button>
            <button onClick={this.clearSelect}>Clear</button>
            <p><input type="text" name="channelId" onKeyPress={this.handleKeyPress} /></p>
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