let $modal;

export default class Modal {
  static $modal_content;
  static $modal_title;
  static $modal;

  static setModalContent(modal_title, modal_content) {
    Modal.show();

    Modal.$modal_content.innerHTML = modal_content;
    Modal.$modal_title.innerHTML = modal_title;
  }

  static clearModalContent() {
    Modal.$modal_content.innerHTML = "";
    Modal.$modal_title.innerHTML = "";
  }

  static appendToModalContent(new_content) {
    Modal.$modal_content.innerHTML += new_content;
  }

  static show() {
    Modal.$modal.classList.remove("d-none");
  }

  static hide() {
    Modal.$modal.classList.add("d-none");
  }
}

function main() {
  Modal.$modal_content = document.querySelector("#modal .modal-content");
  Modal.$modal_title = document.querySelector("#modal .modal-title");
  Modal.$modal = document.getElementById("modal");
}

document.readyState == "complete"
  ? main()
  : document.addEventListener("DOMContentLoaded", main);
