function handleNotifications($id) {
   checkNotifications($id);
   window.setInterval(function(){
      checkNotifications($id);
   }, 2500);
}

$notifications = [];

function checkNotifications($id) {
   $.get('http://localhost:8000/notifications?uid='+$id, function(data) {
      $receivedNotifications = data.split(";");
      if (data!="") {
         for ($i=0; $i<$receivedNotifications.length; $i++)
         {
            $nValue = $receivedNotifications[$i].split("/");
            $nId = $nValue[0];
            $nText = $nValue[1];
            if (!$notifications.some(n => n.id === $nId)) {
               $notifications.push({id: $nId, text: $nText});
               displayNotification($nId, $nText);
            }
         }
   }
   });
}

function displayNotification($nId, $nText) {
   $("<div>").attr({
      id: "n" + $nId,
      class: "notification"
   }).appendTo("body");
   $("#n" + $nId).append("<div id='nTitle" + $nId + "' class='notificationTitle'>Powiadomienie</div><div class='notificationText'>" + $nText + "</div>");
   $("#nTitle" + $nId).append("<a href='http://localhost:8000/notificationread?id=" + $nId + "'><div class='icon icon-checkWhite'></div></a>");
   $("#n" + $nId).css("bottom", ($notifications.length-1)*78+10 + "px");
   $("#n" + $nId).animate({"right": '+=280'});
}
