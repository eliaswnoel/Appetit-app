const labels = document.querySelectorAll('label');
const ingredientForm = document.getElementById('ingredient-form')
const ingFormDivs = ingredientForm.querySelectorAll('div');
const ingredientInput = document.getElementById('id_ingredient');
const addIngredientBtn = document.getElementById('show-ingredient-btn');
const stepsForm = document.getElementById('add-steps');
const stepsInput = document.getElementById('id_instructions');
const addStepsBtn = document.getElementById('add-step-btn');
const reviewInput = document.getElementById('id_text');
const doneIngredient = document.getElementById('done-ingredient');

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
addStyles(reviewInput, 'w-full')
addStyles(ingredientInput, 'bg-card-bg')
addStyles(ingredientInput, 'border-0')
addStyles(ingredientInput, 'rounded-md')
addStyles(ingredientInput, 'w-1/2')
addStyles(ingredientInput, 'm-0')
addStyles(stepsInput, 'bg-card-bg')
addStyles(reviewInput, 'bg-card-bg')


window.onload = () => {
 
  doneIngredient.addEventListener('click', (e) => {
    ingredientForm.style.display = 'none';
    addIngredientBtn.style.display = "inline-flex";
    doneIngredient.style.display = 'none'
  })
  addIngredientBtn.addEventListener('click', (e) => {
    ingredientForm.style.display = 'flex';
    doneIngredient.style.display = "inline-flex";
    addIngredientBtn.style.display = 'none'
  })

  addStepsBtn.addEventListener('click', (e) => {
    stepsForm.style.display = 'block'
    addStepsBtn.style.display = 'none'
  })
  
  
}
