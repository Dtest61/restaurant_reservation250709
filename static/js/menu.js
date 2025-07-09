const { createApp } = Vue;

const MenuApp = {
  data() {
    return {
      menuItems: [
        { id: 1, name: "寿司", description: "新鮮な寿司です", price: 1000 },
        { id: 2, name: "ラーメン", description: "美味しいラーメン", price: 800 }
      ],
    };
  },
  template: `
    <div>
      <h2>メニュー</h2>
      <div v-for="item in menuItems" :key="item.id">
        <h3>{{ item.name }}</h3>
        <p>{{ item.description }}</p>
        <p>¥{{ item.price }}</p>
      </div>
    </div>
  `,
};

createApp(MenuApp).mount("#menu");  // #menuにVueをマウント