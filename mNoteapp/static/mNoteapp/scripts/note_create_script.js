function typeSelected() {
   $("#textnote").attr("hidden", true);
   $("#todonote").attr("hidden", true);
   $("#listnote").attr("hidden", true);
   $("#id_text").val("");
   $("#textnotetext").val("");
   $("#" + $("#id_type").val() + "note").attr("hidden", false);
}

$("#id_type").change(function() {
   typeSelected();
});

function textnoteKeyup() {
   $("#id_text").val($("#textnotetext").val());
}

$todoOptionsCount = 1;
$listOptionsCount = 1;

function addOption($type) {
   $count = $type == "todo" ? ++$todoOptionsCount : ++$listOptionsCount;
   $("<input>").attr({
      type: "text",
      id: $type + "Option" + $count
   }).appendTo("." + $type + "Options");
   $("#" + $type + "Option" + $count).keyup(function() {
      optionKeyup($type);
   });
}

function optionKeyup($type) {
   $("#id_text").val("");
   $count = $type == "todo" ? $todoOptionsCount : $listOptionsCount;
   for ($i = 1; $i <= $count; $i++) {
      if ($.trim($("#" + $type + "Option" + $i).val())!="")
      $("#id_text").val($("#id_text").val() + $("#" + $type + "Option" + $i).val() + ";");
   }
}
