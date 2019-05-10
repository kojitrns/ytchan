// const channelDataCont = ['maincategory','subcategory','channelid','title','viewcount','videocount','subscribercount',
// 'thumbnail_url','description','keywords','uploads_id', 'publishe_date']

const myappAddr = "api/api.php"
const ytAddr = "https://www.googleapis.com/youtube/v3/channels?"
const apiKey = "AIzaSyD3R2gavNlItHEZWTt-_UOMEwFwMN5reiQ"

class Mgr extends React.Component {

  constructor(props) {
    super(props)
    this.state = {channelData: ["abc","def"], selectedChannelId: "none", curCategory: "ニュース",
      selectedCategory: "ニュース", selectedSubCategory: "地震"}
    // this.updateChannelId = this.updateChannelId.bind(this)
    this.onChangeCategorySelector = this.onChangeCategorySelector.bind(this)
    this.onChangeSubCategorySelector = this.onChangeSubCategorySelector.bind(this)
    this.handleKeyPress = this.handleKeyPress.bind(this)
  }

  processChannelData(channelData) {
    var res = []
    channelData.forEach(data =>{
      if(data['maincategory']){
        if(res[data['maincategory']]==null)
          res[data['maincategory']]=[]
        if(res[data['maincategory']][data['subcategory']]==null)
          res[data['maincategory']][data['subcategory']]=[]
        res[data['maincategory']][data['subcategory']].push(data)
      }
    })
    return res
  }

  fetchData = () => {
    console.log("fetchData called")
    fetch(myappAddr)
      .then(res => res.json())
      .then(json => {
        this.setState({channelData: this.processChannelData(json)})
      // console.log(JSON.stringify(myJson));
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
    }).then(res => console.log(res))
  }

  deleteChannel = () => {
    const sendData = {
        opType: 'delete',
        channelid: this.state.selectedChannelId
    }
    this.callApi(sendData)
  }

  moveChannel = () => {
    const sendData = {
          opType: 'move',
          channelid: this.state.selectedChannelId,
          maincategory: this.state.selectedCategory,
          subcategory: this.state.selectedSubCategory
    }
    this.callApi(sendData)
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
    this.fetchData()
    console.log(this.state)
  }

  selecteChannel(channelId){
  	console.log("select_channelId", event)
  	this.setState({selectedChannelId: channelId})
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

  render(){
    console.log("render")

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

      subcategoryArray.forEach(data => {
        channelTable.push(
          <div className="chan-box" onClick={this.selecteChannel.bind(this, data['channelid'])}>
            <img src = {data['thumbnailurl']} />
            <div className="chan-info-box">
              <div className="counter-box">
                <p>{data['viewcount']}</p><p>{data['videocount']}</p><p>{data['subscribercount']}</p>
              </div>
              <div className="detail-box">
                <a href={"https://socialblade.com/youtube/channel/" + data['channelid']} target="_blank"> sbinfo</a>
              </div>
            </div>
            <div className = {data['channelid']!=this.state.selectedChannelId ?"chan-title-box":"selected-title-box"}>
              <a href={"https://www.youtube.com/channel/" + data['channelid']} target="_blank" title={data['channeltitle']}>{data['channeltitle']}</a>
            </div>
          </div>
        )}
      )
      channelPanel.push(<div className="chan-container clearfix">{channelTable}</div>)
    })


    return (
      <div>
        <header className="site-header"><nav><b>カテゴリ:</b>{categoryCont}</nav></header><div className="header-emb"></div>
        <div className="left-panel">{leftPanelCont}</div>
        <div className="main-category-panel"><h2>{this.state.curCategory}</h2>{channelPanel}</div>
        <div className="controlPanel">
          <center>
            <button onClick={this.deleteChannel}>Delete</button>
            <button onClick={this.fetchData}>Update</button>
            <p><select name="mainCategory" value={this.state.selectedCategory} onChange={this.onChangeCategorySelector}>{categorySelectorCont}</select></p>
            <p><select name="subCategory" value={this.state.selectedSubCategory}
            onChange={this.onChangeSubCategorySelector}>{subCategorySelectorCont}</select></p>
            <button onClick={this.moveChannel}>Move</button>
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