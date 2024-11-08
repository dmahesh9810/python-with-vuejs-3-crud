<template>
  <div>
    <h2>Create, Read, Update, Delete</h2>
    <form @submit.prevent="createItem">
      <input type="text" v-model="newItem" placeholder="Enter item" />
      <button type="submit">Add Item</button>
    </form>

    <ul>
      <li v-for="item in items" :key="item.id">
        <span>{{ item.name }}</span>
        <button @click="editItem(item)">Edit</button>
        <button @click="deleteItem(item.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      items: [],
      newItem: '',
      editingItem: null,
    };
  },
  created() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
      try {
        const response = await axios.get('http://localhost:5000/items');
        this.items = response.data;
      } catch (error) {
        console.error("There was an error fetching the items:", error);
      }
    },
    async createItem() {
      if (this.newItem) {
        const response = await axios.post('http://localhost:5000/items', {
          name: this.newItem,
        });
        this.items.push(response.data);
        this.newItem = ''; // Clear input
      }
    },
    async editItem(item) {
      this.editingItem = item;
      this.newItem = item.name; // Set input for editing
    },
    async updateItem() {
      if (this.editingItem) {
        const response = await axios.put(`http://localhost:5000/items/${this.editingItem.id}`, {
          name: this.newItem,
        });
        const index = this.items.findIndex((item) => item.id === this.editingItem.id);
        this.items[index] = response.data;
        this.editingItem = null;
        this.newItem = '';
      }
    },
    async deleteItem(id) {
      await axios.delete(`http://localhost:5000/items/${id}`);
      this.items = this.items.filter((item) => item.id !== id);
    },
  },
  watch: {
    editingItem() {
      if (!this.editingItem) {
        this.newItem = '';
      }
    }
  }
};
</script>

<style scoped>
/* Add some basic styling */
button {
  margin-left: 10px;
}
</style>
