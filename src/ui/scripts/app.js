// This runs as soon as the window loads
window.onload = function() {
    loadProfiles();
};

// 1. Fetch profiles from Python and show them in the sidebar
async function loadProfiles() {
    const profiles = await pywebview.api.load_credentials();
    const sidebar = document.getElementById('sidebar');
    const addButton = document.querySelector('.add-profile-btn');

    // Remove existing profile icons (but keep the + button)
    const existingIcons = document.querySelectorAll('.profile-icon');
    existingIcons.forEach(icon => icon.remove());

    if (profiles && profiles.length > 0) {
        profiles.forEach(profile => {
            const icon = document.createElement('div');
            icon.className = 'profile-icon';
            // Use the first two letters of the name as the icon text
            icon.innerText = profile.display_name.substring(0, 2).toUpperCase();
            icon.title = profile.display_name;
            
            // When clicked, it should tell Python to switch accounts
            icon.onclick = () => selectProfile(profile.uid, profile.display_name);
            
            // Add it to the sidebar before the + button
            sidebar.insertBefore(icon, addButton);
        });
    }
}

// 2. Handle what happens when a profile is clicked
async function selectProfile(uid, name) {
    document.getElementById('view-title').innerText = name;
    document.getElementById('email-list').innerText = "Loading emails...";
    
    // Later, you'll call a Python function here like:
    // const emails = await pywebview.api.get_emails_for_profile(uid);
    // renderEmails(emails);
}

// 3. Placeholder for the modal you'll build later
function showAddProfileModal() {
    document.getElementById('modal-overlay').style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal-overlay').style.display = 'none';
}

// Update your handleAddAccount to close the modal when done
async function handleAddAccount() {
    const name = document.getElementById('display-name').value;
    const email = document.getElementById('email-input').value;
    const pass = document.getElementById('pass-input').value;
    const host = document.getElementById('host-input').value;

    const result = await pywebview.api.save_credentials(name, email, pass, host);
    
    if (result.status === "success") {
        closeModal();
        loadProfiles(); // Refresh the sidebar
    } else {
        alert("Error: " + result.message);
    }
}