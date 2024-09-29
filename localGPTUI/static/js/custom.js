function openFileSelection() {
    const fileInput = document.getElementById("fileInput");
    fileInput.accept = ".csv, .pdf, .txt, .doc";
    fileInput.click();
    fileInput.addEventListener("change", handleFileSelection);
  }
  
  function handleFileSelection(event) {
    const uploadModal = new bootstrap.Modal(document.getElementById("uploadModal"));
    uploadModal.show();
  }
  
  function submitForm(action) {
    var form = document.getElementById("uploadForm");
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "action";
    input.value = action;
    form.appendChild(input);
  
    $("#uploadModal").on("hidden.bs.modal", function () {
      $("#ingesting-modal").modal("show");
    });
  
    form.submit();
  }
  
  function submitPromptForm() {
    $("#responseModal").modal("show");
    setTimeout(function () {
      document.getElementById("promptForm").submit();
    }, 5);
  }
  
  document.getElementById("searchInput").addEventListener("keydown", function (event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      submitPromptForm();
    }
  });
  
  document.addEventListener("DOMContentLoaded", function() {
    var chatbotTrigger = document.getElementById("chatbotTrigger");
    chatbotTrigger.addEventListener("click", function() {
      var chatbotContainer = document.getElementById("chatbotContainer");
      if (chatbotContainer.style.display === "none") {
        chatbotContainer.style.display = "flex";
      } else {
        chatbotContainer.style.display = "none";
      }
    });
  });
  