// src/composables/useMobileFooter.js
import { onMounted, onBeforeUnmount } from 'vue';

export function useMobileFooter() {
  const mobileQuery = window.matchMedia("(max-width: 768px)");
  let mobileFooter = null;

  const moveFooter = () => {
    const sidebar = document.querySelector(".sidebar");
    const layout = document.querySelector(".layout-container");

    if (!sidebar || !layout) return;

    const originalFooter = sidebar.querySelector(".bottom-area");

    // 只在手機版且未建立 mobileFooter
    if (mobileQuery.matches) {
      if (originalFooter && !mobileFooter) {
        // clone footer
        mobileFooter = originalFooter.cloneNode(true);
        mobileFooter.classList.add("mobile-footer");

        // append to layout-container
        layout.appendChild(mobileFooter);

        // hide original
        originalFooter.style.display = "none";
      }
    } else {
      // 回到桌面版：恢復 sidebar footer
      if (mobileFooter) {
        mobileFooter.remove();
        mobileFooter = null;
      }
      if (originalFooter) {
        originalFooter.style.display = "";
      }
    }
  };

  onMounted(() => {
    moveFooter();
    mobileQuery.addEventListener("change", moveFooter);
  });

  onBeforeUnmount(() => {
    mobileQuery.removeEventListener("change", moveFooter);
  });
}