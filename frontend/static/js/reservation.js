
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("reservation-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = {
            name: document.querySelector("[name=name]").value,
            email: document.querySelector("[name=email]").value,
            phone: document.querySelector("[name=phone]").value,
            party_size: document.querySelector("[name=party_size]").value, // numeric string
            date: document.querySelector("[name=date]").value,
            time: document.querySelector("[name=time]").value,
            notes: document.querySelector("[name=notes]").value
        };

        try {
            const response = await fetch("/create-reservation", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                alert("Reservation created successfully!");
                form.reset();
            } else {
                alert("Failed to create reservation: " + result.message);
            }
        } catch (err) {
            console.error(err);
            alert("An error occurred while creating the reservation.");
        }
    });
});