const showFolders = document.getElementById('show-folders');
const folderOptions = document.getElementById('folder-options');
const foldersPopUp = document.getElementById('folders-popup');

window.onload = () => {
  
  
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