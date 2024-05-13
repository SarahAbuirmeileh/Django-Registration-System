const addCourseToSchedule = async (studentId, courseId) => {
    const URL = `http://127.0.0.1:8000/student/${studentId}/course/${courseId}/`;

    try {
        const response = await fetch(URL, {
            method: 'PUT',
        });

        const data = await response.json();
        alert("Course added successfully!");
    } catch (error) {
        console.log(error)
        alert("Error adding course: " + error);
    }
};

document.getElementById('add-course').addEventListener('click', function() {
    const studentId = "1";
    const courseId = "123";

    addCourseToSchedule(studentId, courseId);
});
