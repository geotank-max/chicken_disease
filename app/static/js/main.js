document.addEventListener("DOMContentLoaded", () => {
  const pwd = document.querySelector('input[name="password"]');
  if (!pwd) return;

  pwd.addEventListener("input", () => {
    const msg = document.querySelector("#passwordHelp");
    if (!msg) return;

    const v = pwd.value;
    const strong =
      v.length >= 8 &&
      /[A-Z]/.test(v) &&
      /[a-z]/.test(v) &&
      /[0-9]/.test(v) &&
      /[!@#$%^&*(),.?":{}|<>_\-+=]/.test(v);

    msg.textContent = strong
      ? "ពាក្យសម្ងាត់រឹងមាំ ✅"
      : "ប្រើយ៉ាងហោចណាស់ ៨ តួអក្សរ រួមមានអក្សរធំ តូច លេខ និងសញ្ញាពិសេស";
    msg.className = strong ? "form-text text-success" : "form-text text-danger";
  });
});
