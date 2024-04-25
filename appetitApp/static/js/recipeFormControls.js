const labels = document.querySelectorAll('label');
const ingredientForm = document.getElementById('ingredient-form')
const ingFormDivs = ingredientForm.querySelectorAll('div');
const ingredientInput = document.getElementById('id_ingredient');
const addIngredientBtn = document.getElementById('show-ingredient-btn');
const stepsForm = document.getElementById('add-steps');
const stepsInput = document.getElementById('id_instructions');
const addStepsBtn = document.getElementById('add-step-btn');
const showFolders = document.getElementById('show-folders');
const folderOptions = document.getElementById('folder-options');
const foldersPopUp = document.getElementById('folders-popup');
// const reviewForm = document.getElementById('review-form');
// const reviewInput = reviewForm.getElementById('id_text');
const editBtn = document.querySelector('#edit-btn');


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


const show = (div) => {
  div.classList.add('flex')
  div.classList.remove('hidden')
}

const hide = (div) => {
  div.classList.remove('flex')
  div.classList.add('hidden')
}

window.onload = () => {
  addStyles(stepsInput, 'w-full')
  // addStyles(reviewInput, 'w-full')
  addStyles(ingredientInput, 'bg-card-bg')
  addStyles(ingredientInput, 'border-0')
  addStyles(ingredientInput, 'rounded-md')
  addStyles(ingredientInput, 'w-1/2')
  addStyles(ingredientInput, 'm-0')
  addStyles(stepsInput, 'bg-card-bg')
  // addStyles(reviewInput, 'bg-card-bg')
 
  editBtn.addEventListener('click', (e) => {
    console.log(e.target)
    addIngredientBtn.style.display = 'flex'
    addStepsBtn.style.display = 'block'
  })

  addIngredientBtn.addEventListener('click', (e) => {
    ingredientForm.style.display = 'flex';
    addIngredientBtn.classList.add('hidden')
  })

  addStepsBtn.addEventListener('click', (e) => {
    stepsForm.style.display = 'block'
    addStepsBtn.style.display = 'none'
  })
  
  let click = 1

  showFolders.addEventListener('click', (e) => {
    if (click===1) {
      folderOptions.classList.remove('hidden');
      folderOptions.classList.add('flex');
      showFolders.classList.add('rotate-45');
      foldersPopUp.classList.add('absolute')
    }
    
    if (click === -1) {
      foldersPopUp.classList.remove('absolute')
      folderOptions.classList.remove('absolute')
      folderOptions.classList.add('hidden');
      folderOptions.classList.remove('flex');
      showFolders.classList.remove('rotate-45');
    }
    
    click *=-1
  })
  
}
