let input_search = "";

function handle_search(event) {
    event.preventDefault(); // ✅ FIXED: You had a typo here
    input_search = document.getElementById("default-search").value;
    handleApi();
}

function handleApi() {
    let url = "/filter-student-api/?search=" + input_search;

    $.ajax({
                url: url,
                type: "GET",
                success: function(data) {
                        console.log("ekram");
                        console.log(data);

                        const students = data.Students;
                        var tableBody = document.getElementById("student_table");
                        var new_data = "";

                        for (let index = 0; index < students.length; index++) {
                            let student = students[index];

                            new_data += `
                    <tr id="row_${student.id}" class="text-center border-t">
                        <td class="px-4 py-2 border">
                            ${student.profile_pic 
                                ? `<img src="${student.profile_pic}" alt="Profile" class="w-16 h-16 rounded-full mx-auto" />` 
                                : `<span class="text-gray-400">No Image</span>`}
                        </td>
                        <td class="px-4 py-2 border">${student.firstname} ${student.lastname}</td>
                        <td class="px-4 py-2 border">${student.roll_no}</td>
                        <td class="px-4 py-2 border">${student.dept}</td>
                        <td class="px-4 py-2 border">${student.address}</td>
                        <td class="px-4 py-2 border space-x-2">
                            <a href="/student-data/${student.id}/" class="text-blue-600 hover:underline">Edit</a>
                            <button onclick="DeleteStudent(${student.id})" class="text-red-600 hover:underline">Delete</button>
                        </td>
                    </tr>
                `;
            }

            tableBody.innerHTML = new_data;
        },
        error: function(xhr, status, error) {
            console.error("Error loading student data:", error);
        }
    });
}