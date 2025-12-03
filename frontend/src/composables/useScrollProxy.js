import { onMounted, onBeforeUnmount } from "vue";

export function useScrollProxy() {
  let contentArea = null;

  const handleWheel = (e) => {
    if (!contentArea) return;
    contentArea.scrollTop += e.deltaY; // 滾動 right content
    e.preventDefault(); // 禁止 body 捲動
  };

  onMounted(() => {
    contentArea = document.querySelector(".main-content");

    // 全域監聽，不只 sidebar
    window.addEventListener("wheel", handleWheel, { passive: false });
  });

  onBeforeUnmount(() => {
    window.removeEventListener("wheel", handleWheel);
  });
}