// code reference from the W3schools
function dropDownMenu() {
	//toggle the button between show and not show the drop down menu
	document.getElementById("dropDownMenu").classList.toggle("show");
}

window.onclick = function(event) 
{
	if (!event.target.matches('.btnImg')) 
	{
		var dropDowns = document.getElementsByClassName("dropDownContent");
		for (var i=0; i<dropDowns.length; i++) 
		{
			var openDropdown = dropDowns[i];
			if (openDropdown.classList.contains('show')) 
			{
				openDropdown.classList.remove('show');
			}
		}
	}
}

//pop up form in index.html
// to upload new post
function openForm() {
	document.getElementById("uploadForm").style.display = "block";
	document.getElementById("formOverlay").style.display = "block";
}

function closeForm() {
	document.getElementById("uploadForm").style.display = "none";
	document.getElementById("formOverlay").style.display = "none";
}

window.onclick = function(event) {
    var uploadForm = document.getElementById("uploadForm");
    var overlay = document.getElementById("formOverlay");
    
    if (event.target == overlay) {
        uploadForm.style.display = "none";
        overlay.style.display = "none";
    }
}

function dropDownDelete() {
	//toggle the button between show and not show the drop down delete menu
	document.getElementById("dropDownDelete").classList.toggle("showDelete");
}

window.onclick = function(event) 
{
	if (!event.target.matches('.deleteImg')) 
	{
		var dropDowns = document.getElementsByClassName("dropDownDeleteContent");
		for (var i=0; i<dropDowns.length; i++) 
		{
			var openDropdown = dropDowns[i];
			if (openDropdown.classList.contains('showDelete')) 
			{
				openDropdown.classList.remove('showDelete');
			}
		}
	}
}
// code reference from the W3schools
