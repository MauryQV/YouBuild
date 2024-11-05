// static/js/validaciones.js
function validateSearch() {
    const searchField = document.querySelector('input[name="q"]');
    if (searchField.value.trim() === "") {
      alert("Por favor, ingrese un término de búsqueda.");
      return false;
    }
    return true;
  }  