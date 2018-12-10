function initialize() {
   $("#textnote").attr("hidden", true);
   $("#todonote").attr("hidden", true);
   $("#listnote").attr("hidden", true);
   $noteType = $("#id_type").val();
   $("#" + $noteType + "note").attr("hidden", false);
   if ($noteType == "text") {
      $("#textnotetext").val($("#id_text").val());
   }
   else {
      $fieldArr = $("#id_text").val().split(";");
      for ($i = 0; $i < $fieldArr.length-2; $i++)
         addOption($noteType);
      for ($i = 0; $i < $fieldArr.length-1; $i++)
         $("#" + $noteType + "Option" + ($i+1)).val($fieldArr[$i].replace("*", ""));
   }
}
