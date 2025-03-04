import { getAuth, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js';

const auth = getAuth();

onAuthStateChanged(auth, (user) => {
    if (user) {
        // User is signed in
        window.location.href = '/dashboard';
    }
});
