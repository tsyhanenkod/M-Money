// const triggerInputs = document.querySelectorAll('.trigger_input');
//
// // Добавляем обработчик события "click" для каждого элемента
// triggerInputs.forEach(function(input) {
//   input.addEventListener('click', function() {
//     // Проверяем, имеет ли текущий элемент активный класс
//     const isActive = this.parentElement.classList.contains('active');
//
//     // Если текущий элемент не активный, обновляем состояние переключателей
//     if (!isActive) {
//       // Добавляем класс "active" только текущему элементу
//       this.parentElement.classList.add('active');
//
//       // Удаляем класс "active" у всех элементов, кроме текущего
//       triggerInputs.forEach(function(otherInput) {
//         if (otherInput !== input) {
//           otherInput.parentElement.classList.remove('active');
//         }
//       });
//     }
//   });
// });

const triggerInputs = document.querySelectorAll('.trigger_input');

// Добавляем обработчик события "click" для каждого элемента
triggerInputs.forEach(function(input) {
  input.addEventListener('click', function() {
    // Проверяем, имеет ли текущий элемент активный класс
    const isActive = this.parentElement.classList.contains('active');

    // Если текущий элемент не активный, обновляем состояние переключателей
    if (!isActive) {
      // Добавляем класс "active" только текущему элементу
      this.parentElement.classList.add('active');

      // Удаляем класс "active" у всех элементов, кроме текущего
      triggerInputs.forEach(function(otherInput) {
        if (otherInput !== input) {
          otherInput.parentElement.classList.remove('active');
        }
      });
    }

    // Обновляем значение переключателя radio
    const value = this.value;
    const radioInput = document.querySelector(`input[value="${value}"]`);
    radioInput.checked = true;
  });
});

