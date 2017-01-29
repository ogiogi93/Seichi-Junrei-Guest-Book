var apis = {};

(function() {
  var ep = "http://pwc-seichi-jyunrei.ogiogi93.com/api/bot_chat?";
  var chs = {"1": "Josikousei", "2": "akachan", "3": "utyuujin"};
  
  apis.send = function(utt, v, ul) {
     var url = ep + "utt=" + utt + "&ch=" + chs[v]
     $.ajax({
        type: 'GET',
        url: ep,
        dataType: 'text',
        success: function(response){
            ul.append("<li>" + response + "</li>")
            return response;
        },
        error: function(response){
            return response;
        }});
  }

  apis.rep = function() {
    var c = $('.txt-comment').val();
    var v = $('.i-r:checked').val();
    var ul = $('.com' + v);
    ul.append("<li>" + c + "</li>")
    rs = apis.send(c, v, ul);
  }

})();
