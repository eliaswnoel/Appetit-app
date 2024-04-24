// cache
const recipeForm = document.getElementById('recipe-form');
const formDivs = recipeForm.querySelectorAll('div');
const labels = recipeForm.querySelectorAll('label')
//  input fields
const recipeName = document.getElementById('id_name');
const recipeDescription = document.getElementById('id_description');
const inputArr = [recipeName, recipeDescription]

// style constructors --------------------------------------
// add styles to a class constructor 
const addStyles = (div, type) => {
  div.classList.add(type)
} 

const addPlaceholder = (div, text) => {
  div.placeholder = text
}

// add styles to every input in inputArr
addStyles(recipeName, 'form-input');
addStyles(recipeName, 'w-full');
addStyles(recipeDescription, 'bg-neutral-50')


addPlaceholder(recipeName, 'Recipe Name');
addPlaceholder(recipeDescription, 'Add a description for your recipe')

for (let label of labels) {
label.style.display = 'none'
}

for (let div of formDivs) {
  addStyles(div, 'w-full')
}


