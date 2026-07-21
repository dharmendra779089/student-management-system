// State Management
let students = [];
let editModeId = null;

// DOM Elements
const studentForm = document.getElementById('student-form');
const formSubmitBtn = document.getElementById('form-submit-btn');
const formCancelBtn = document.getElementById('form-cancel-btn');
const formTitle = document.getElementById('form-title');
const searchInput = document.getElementById('search-input');
const courseFilter = document.getElementById('course-filter');
const themeToggle = document.getElementById('theme-toggle');

// Stat Elements
const statTotal = document.getElementById('stat-total');
const statAverage = document.getElementById('stat-average');
const statHighest = document.getElementById('stat-highest');
const statLowest = document.getElementById('stat-lowest');
const studentTableBody = document.getElementById('student-table-body');
const toastContainer = document.getElementById('toast-container');

// App Initialization
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    loadDashboard();
    setupEventListeners();
});

// Event Listeners setup
function setupEventListeners() {
    studentForm.addEventListener('submit', handleFormSubmit);
    formCancelBtn.addEventListener('click', resetForm);
    searchInput.addEventListener('input', filterStudents);
    courseFilter.addEventListener('change', filterStudents);
    themeToggle.addEventListener('click', toggleTheme);
}

// Fetch dashboard data
async function loadDashboard() {
    await fetchStudents();
    await fetchStats();
    populateCourseFilter();
    renderStudentTable(students);
}

// Fetch all students
async function fetchStudents() {
    try {
        const response = await fetch('/api/students');
        if (!response.ok) throw new Error('Failed to fetch students.');
        students = await response.ok ? await response.json() : [];
    } catch (error) {
        showToast('Error loading student records.', 'error');
        console.error(error);
    }
}

// Fetch stats
async function fetchStats() {
    try {
        const response = await fetch('/api/stats');
        if (!response.ok) throw new Error('Failed to fetch stats.');
        const stats = await response.json();
        
        statTotal.textContent = stats.total_students;
        statAverage.textContent = stats.average_marks ? `${stats.average_marks}%` : 'N/A';
        
        if (stats.highest_student) {
            statHighest.textContent = `${stats.highest_student.name} (${stats.highest_student.marks}%)`;
        } else {
            statHighest.textContent = 'None';
        }
        
        if (stats.lowest_student) {
            statLowest.textContent = `${stats.lowest_student.name} (${stats.lowest_student.marks}%)`;
        } else {
            statLowest.textContent = 'None';
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Render student table rows
function renderStudentTable(studentsToRender) {
    studentTableBody.innerHTML = '';
    
    if (studentsToRender.length === 0) {
        studentTableBody.innerHTML = `
            <tr>
                <td colspan="7" class="empty-state">
                    <div class="empty-state-icon">📁</div>
                    <div class="empty-state-title">No Students Found</div>
                    <p>Add a student or adjust your search filter</p>
                </td>
            </tr>
        `;
        return;
    }
    
    studentsToRender.forEach(student => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${escapeHTML(student.student_id)}</strong></td>
            <td>${escapeHTML(student.name)}</td>
            <td>${escapeHTML(String(student.age))}</td>
            <td>${escapeHTML(student.gender)}</td>
            <td>${escapeHTML(student.course)}</td>
            <td><strong>${escapeHTML(String(student.marks))}%</strong></td>
            <td><span class="badge badge-grade-${student.grade.toLowerCase()}">Grade ${escapeHTML(student.grade)}</span></td>
            <td>
                <div style="display:flex; gap:0.5rem;">
                    <button class="btn-icon-only edit" onclick="startEditStudent('${escapeHTML(student.student_id)}')" title="Edit Student">✏️</button>
                    <button class="btn-icon-only delete" onclick="deleteStudent('${escapeHTML(student.student_id)}')" title="Delete Student">🗑️</button>
                </div>
            </td>
        `;
        studentTableBody.appendChild(tr);
    });
}

// Populate course list for filter dropdown
function populateCourseFilter() {
    const courses = [...new Set(students.map(s => s.course))];
    const currentSelection = courseFilter.value;
    
    courseFilter.innerHTML = '<option value="">All Courses</option>';
    courses.forEach(course => {
        const option = document.createElement('option');
        option.value = course;
        option.textContent = course;
        if (course === currentSelection) option.selected = true;
        courseFilter.appendChild(option);
    });
}

// Handle Form Submissions (Add / Edit)
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const idInput = document.getElementById('student-id');
    const nameInput = document.getElementById('student-name');
    const ageInput = document.getElementById('student-age');
    const genderInput = document.getElementById('student-gender');
    const courseInput = document.getElementById('student-course');
    const marksInput = document.getElementById('student-marks');
    
    const payload = {
        student_id: idInput.value.trim(),
        name: nameInput.value.trim(),
        age: parseInt(ageInput.value),
        gender: genderInput.value,
        course: courseInput.value.trim(),
        marks: parseFloat(marksInput.value)
    };
    
    if (editModeId) {
        // Edit mode API PUT call
        try {
            const response = await fetch(`/api/students/${editModeId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const result = await response.json();
            if (response.ok) {
                showToast('Student record updated successfully!', 'success');
                resetForm();
                loadDashboard();
            } else {
                showToast(result.error || 'Failed to update student.', 'error');
            }
        } catch (error) {
            showToast('Network error updating student.', 'error');
        }
    } else {
        // Add mode API POST call
        try {
            const response = await fetch('/api/students', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const result = await response.json();
            if (response.ok) {
                showToast('Student added successfully!', 'success');
                resetForm();
                loadDashboard();
            } else {
                showToast(result.error || 'Failed to add student.', 'error');
            }
        } catch (error) {
            showToast('Network error adding student.', 'error');
        }
    }
}

// Start Edit Mode
window.startEditStudent = function(studentId) {
    const student = students.find(s => s.student_id === studentId);
    if (!student) return;
    
    editModeId = studentId;
    
    // Fill form inputs
    const idInput = document.getElementById('student-id');
    idInput.value = student.student_id;
    idInput.disabled = true; // Cannot edit the ID
    
    document.getElementById('student-name').value = student.name;
    document.getElementById('student-age').value = student.age;
    
    const genderSelect = document.getElementById('student-gender');
    genderSelect.value = student.gender;
    genderSelect.disabled = true; // Gender updates not permitted per guidelines
    
    document.getElementById('student-course').value = student.course;
    document.getElementById('student-marks').value = student.marks;
    
    // Update headers and actions
    formTitle.innerHTML = '✏️ Edit Student';
    formSubmitBtn.innerHTML = '<span>💾</span> Update Student';
    formCancelBtn.style.display = 'inline-flex';
};

// Reset Form State
function resetForm() {
    editModeId = null;
    studentForm.reset();
    
    const idInput = document.getElementById('student-id');
    idInput.disabled = false;
    
    const genderSelect = document.getElementById('student-gender');
    genderSelect.disabled = false;
    
    formTitle.innerHTML = '🎓 Add New Student';
    formSubmitBtn.innerHTML = '<span>➕</span> Add Student';
    formCancelBtn.style.display = 'none';
}

// Delete Student records
window.deleteStudent = async function(studentId) {
    if (!confirm(`Are you sure you want to delete student ID: ${studentId}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/students/${studentId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        if (response.ok) {
            showToast('Student deleted successfully.', 'success');
            loadDashboard();
            if (editModeId === studentId) resetForm();
        } else {
            showToast(result.error || 'Failed to delete student.', 'error');
        }
    } catch (error) {
        showToast('Network error deleting student.', 'error');
    }
};

// Client-side Real-time Search and Filter logic
function filterStudents() {
    const query = searchInput.value.toLowerCase().trim();
    const course = courseFilter.value;
    
    const filtered = students.filter(student => {
        const matchesSearch = student.name.toLowerCase().includes(query) || 
                              student.student_id.toLowerCase().includes(query) ||
                              student.course.toLowerCase().includes(query);
        const matchesCourse = course === '' || student.course === course;
        return matchesSearch && matchesCourse;
    });
    
    renderStudentTable(filtered);
}

// Custom Toast notifications
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? '✅' : '❌';
    toast.innerHTML = `<span>${icon}</span> <span>${escapeHTML(message)}</span>`;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s reverse forwards';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Local Theme Storage Setup
function initTheme() {
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme === 'dark' || (!storedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.body.classList.add('dark-theme');
        themeToggle.innerHTML = '☀️';
    } else {
        document.body.classList.remove('dark-theme');
        themeToggle.innerHTML = '🌙';
    }
}

function toggleTheme() {
    if (document.body.classList.contains('dark-theme')) {
        document.body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
        themeToggle.innerHTML = '🌙';
    } else {
        document.body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
        themeToggle.innerHTML = '☀️';
    }
}

// Simple HTML escaping helper
function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}
