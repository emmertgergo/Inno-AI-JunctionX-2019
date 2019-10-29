console.log('Content Switch');
$('.post_emotion').click(post_emotion);
var next_content_url = JSON.parse(document.getElementById('next_content_url').textContent);
var vid = document.getElementById("myVideo");
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

// Functions on key down events (Enter,Right Arrow,Left Arrow)
document.onkeydown = function(event) {
    if (event.key === 'ArrowRight'){
        window.location.pathname = next_content_url;
    }
    else if (event.key === 'Enter'){

    }
};

if(vid != null){
  vid.onended = function() {
   window.location.pathname = next_content_url;
};
}


function post_emotion(){
    post_emotion_ajax(window.location.href,this.getAttribute('id'))
}

function post_emotion_ajax(url_, id){

    $.ajax({
      url: url_,
          data: {'ID' : id, csrfmiddlewaretoken: csrftoken},
          dataType: 'json',
          type: 'POST',
          success: function(){
            window.location.href= next_content_url;
          },
        })

}


console.log(window.location.href);
if(window.location.href.indexOf("end") > -1){
    console.log("timer active");
    setTimeout(function(){ window.location.href= next_content_url; }, 3000);
}
