// This runs as soon as the window loads
window.addEventListener('pywebviewready', function() {
    refreshSidebar();
});

// 2. Handle what happens when a profile is clicked
async function selectProfile(uid, name) {
    document.getElementById('view-title').innerText = name;
    document.getElementById('email-list').innerText = "Loading emails...";
    const emails = await fetchEmailsForProfile(uid);
    renderEmails(emails);
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
    pass = document.getElementById('pass-input').value;
    const pass = pass.replaceAll(" ", "");
    const host = document.getElementById('host-input').value;

    const result = await pywebview.api.save_credentials(name, email, pass, host);
    
    if (result.status === "success") {
        closeModal();
        refreshSidebar(); // Refresh the profile list
    } else {
        alert("Failed to add profile: " + result.message);
    }
}

async function refreshSidebar() {
    const sidebarContainer = document.getElementById('sidebar-profiles'); // Make sure you have this ID in your HTML
    
    // 1. Call your exposed Python function
    const profiles = await pywebview.api.load_credentials();
    
    // 2. Clear the current list (to avoid duplicates)
    sidebarContainer.innerHTML = '';
    
    // 3. Loop through the profiles and create the "Premium" buttons
    profiles.forEach(profile => {
        const profileWrapper = document.createElement('div');
        profileWrapper.className = 'sidebar-button'; 
        
        const initial = profile.name ? profile.name[0].toUpperCase() : profile.email[0].toUpperCase();
        
        // We put the icon AND the name inside the wrapper
        profileWrapper.innerHTML = `
            <div class="profile-icon">${initial}</div>
        `;
        
        profileWrapper.onclick = () => selectProfile(profile.id, profile.name);
        sidebarContainer.appendChild(profileWrapper);
    });
}

async function fetchEmailsForProfile(uid) {
    const email_address = await pywebview.api.get_email_address(uid);
    const password = await pywebview.api.get_email_password(uid);
    const imap_host = await pywebview.api.get_email_host(uid);

    const emails = await pywebview.api.sync_emails(imap_host, email_address, password);
    return emails;
}

async function renderEmails(emails) {
    const emailListContainer = document.getElementById('email-list');
    emailListContainer.innerHTML = ''; // Clear existing emails
    emails.forEach(email => {
        const emailItem = document.createElement('div');
        emailItem.className = 'email-item';
        emailItem.innerHTML = `
            <div class="email-subject">${email.subject}</div>
            <div class="email-sender">From: ${email.from}</div>
            <div class="email-date">Date: ${email.date}</div>
            <div class="email-snippet">${email.snippet}</div>
        `;
        emailListContainer.appendChild(emailItem);
    });
}