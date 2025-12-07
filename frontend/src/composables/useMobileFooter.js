import { onMounted, onBeforeUnmount, watch } from 'vue';

export function useMobileFooter(updatedTimeRef) {
  const mobileQuery = window.matchMedia("(max-width: 768px)");
  let mobileFooter = null;

  const injectFooterHTML = () => {
    if (!mobileFooter) return;

    const updatedString = updatedTimeRef.value || "-";

    const socialIcons = document.querySelector(".sidebar .social-icons");
    const iconsHTML = socialIcons ? socialIcons.innerHTML : "";

    mobileFooter.innerHTML = `
      <div class="inner-content social-icons d-flex align-items-center mt-3">
        ${iconsHTML}
      </div>
      <p class="last-updated mt-2 text-secondary small">
        Last updated: ${updatedString}
      </p>
    `;
  };

  const moveFooter = () => {
    const sidebar = document.querySelector(".sidebar");
    const layout = document.querySelector(".layout-container");
    if (!sidebar || !layout) return;

    const originalFooter = sidebar.querySelector(".bottom-area");

    // ---- MOBILE MODE ----
    if (mobileQuery.matches) {
      if (!mobileFooter) {
        mobileFooter = document.createElement("div");
        mobileFooter.className = "bottom-area mobile-footer";
        layout.appendChild(mobileFooter);
        injectFooterHTML();
      }

      if (originalFooter) originalFooter.style.display = "none";
    }
    // ---- DESKTOP MODE ----
    else {
      if (mobileFooter) {
        mobileFooter.remove();
        mobileFooter = null;
      }
      if (originalFooter) originalFooter.style.display = "";
    }
  };

  onMounted(() => {
    moveFooter();
    mobileQuery.addEventListener("change", moveFooter);

    // ⭐ 當 updatedTime 改變 → 即時更新 footer 顯示
    watch(updatedTimeRef, () => {
      injectFooterHTML();
    });
  });

  onBeforeUnmount(() => {
    mobileQuery.removeEventListener("change", moveFooter);
  });
}