const { createApp } = Vue;

const HomeApp = {
  data() {
    return {
      message: "SUMI base やおや 浜松店 予約サイトへようこそ！",
    };
  },
  mounted() {
    console.log("Vueアプリがマウントされました！");  // マウント確認用のログ
  },
  template: `<div>{{ message }}</div>`,
};

createApp(HomeApp).mount("#app");  // #appにVueをマウント