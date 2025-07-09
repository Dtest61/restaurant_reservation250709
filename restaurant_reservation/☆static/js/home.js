const { createApp } = Vue;

const HomeApp = {
  data() {
    return {
      message: "居酒屋予約サイトへようこそ！",
    };
  },
  template: `<div>{{ message }}</div>`,
};

createApp(HomeApp).mount("#app");  // #appにVueをマウント