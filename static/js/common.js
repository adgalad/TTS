function timeConverter(UNIX_timestamp){
      var a = new Date(UNIX_timestamp * 1000);
      var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      var year = a.getFullYear();
      var month = months[a.getMonth()];
      var date = a.getDate();
      var hour = a.getHours();
      var min = a.getMinutes();
      var sec = a.getSeconds();
      var time = date + '/' + month + '/' + year + ' ' + hour + ':' + min + ':' + sec ;
      return time;
}

function play(url){
      var xhr = new XMLHttpRequest();
      xhr.open('HEAD', url, false);
      xhr.send();
       
      if (xhr.status == "404") {
          alert("Error: El audio no existe.")
      }   

      var audio = new Audio(url);
      audio.play();

}

function file_field(){
      var type = $("#id_type").val();
      if (type != '' && type != 'new'){
          if (type == 'existant'){
              $('#id_audio').show().prop('disabled', false)
              $('#id_file').hide().prop('disabled', true)
          } else {
              $('#id_file').show().prop('disabled', false)
              $('#id_audio').hide().prop('disabled', true)
          }
      } else {
          $('#id_file').hide().prop('disabled', true)
          $('#id_audio').hide().prop('disabled', true)
      }
}


const textarea = $("#id_text")
function synthesize(){
    host = '0.0.0.0:8000'
    url = "http://"+host+"/api/processAudio/test.mp3?text="+textarea.val()
    $('audio #source').attr('src', url);
    $('audio').get(0).load();
    $('audio').get(0).play();
};


function showModal(){
    if (textarea.val()){
        $('#popup').modal('show')
    } else{
        alert("Debe introducir un texto antes de continuar.")
    }
    
}

var lastFocus;

function onclickmenu(e, tag, attr, value) {
    // do whatever you want here
    e.preventDefault();
    e.stopPropagation();
    setTimeout(function() {
        textarea.focus()
        addTag(tag, attr, value)
    }, 10);

    return(false);
};

function insertAtCursor(tag, endtag) {
    //IE support
    // if (document.selection) {
    //     textarea.focus();
    //     sel = document.selection.createRange();
    //     sel.text = tag;
    // }
    //MOZILLA and others

    if (textarea.prop("selectionStart") || textarea.prop("selectionStart") == '0') {
        var startPos = textarea.prop("selectionStart")
        var endPos = textarea.prop("selectionEnd")
        var startStr = textarea.val().substring(0, startPos)
        var selection = textarea.val().substring(startPos, endPos)
        var endStr = textarea.val().substring(endPos, textarea.val().length)
        textarea.val(startStr + tag + selection + endtag + endStr)
        textarea.prop("selectionStart", startPos + tag.length + selection.length + endtag.length)
        textarea.prop("selectionEnd", startPos + tag.length + selection.length + endtag.length)
    } else {
        textarea.val(tag);
    }
}

function addTag(tag, attr, value){
    tagString = '<' + tag + ' ' + attr + '="' + value + '">'
    endtag = '</' + tag + '>'
    insertAtCursor(tagString, endtag)
}