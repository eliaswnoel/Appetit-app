const labels = document.querySelectorAll('label');
const ingredientForm = document.getElementById('ingredient-form')
const ingFormDivs = ingredientForm.querySelectorAll('div');
const ingredientInput = document.getElementById('id_ingredient');
const addIngredientBtn = document.getElementById('show-ingredient-btn');
const stepsForm = document.getElementById('add-steps');
const stepsInput = document.getElementById('id_instructions');
const addStepsBtn = document.getElementById('add-step-btn');


const addStyles = (div, type) => {
  div.classList.add(type)
} 

const addPlaceholder = (div, text) => {
  div.placeholder = text
}

for (let label of labels) {
  label.style.display = 'none'
}

for (let div of ingFormDivs) {
  addStyles(div, 'w-full')
}

addStyles(stepsInput, 'w-full')
addStyles(ingredientInput, 'form-input');
addStyles(ingredientInput, 'w-full');
addStyles(stepsInput, 'bg-card-bg')


window.onload = () => {
  ingredientForm.style.display = 'none'
  stepsForm.style.display = 'none'
  
  addIngredientBtn.addEventListener('click', (e) => {
    ingredientForm.style.display = 'flex';
  })

  addStepsBtn.addEventListener('click', (e) => {
    stepsForm.style.display = 'flex'
  })
  
  
}
