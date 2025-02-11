const RegistrationPage = {
  template: `
    <div class="container mt-4 mb-4">
      <div class="card mb-4">
        <div class="card-body">
          <form @submit.prevent="handleSubmit" id="user_registration">
            <h1 class="text-center"><u>User Registration</u></h1>
            <div>(* : Required)</div>
            <h4>Username*</h4>
            <input type="text" v-model="formData.username" placeholder="Type Username" class="form-control" required>
            
            <div class="mb-2 mt-2"><h4>Email*</h4>
            <input type="email" v-model="formData.email" placeholder="Type Email" class="form-control" required></div>
            
            <h4 class="mt-2">Password*</h4>
            <input type="password" v-model="formData.password" placeholder="Type Password" class="form-control" required>
            
            <h4 class="mt-2">Profile Picture (Allowed Types = ['.jpg', '.jpeg', '.png'])</h4>
            <div class="d-flex">
              <input type="file" ref="fileInput" @change="handleFileUpload" class="form-control" style="width: 500px;">
              <button class="btn btn-outline-secondary ms-2" type="button" @click="clearImage">C</button>
            </div>

            <button type="submit" class="btn btn-outline-success mb-3 mt-3">Register</button>
          </form>
          <router-link to="/user/login" class="btn btn-outline-primary mt-2">Go to Login</router-link>
        </div>
      </div>
    </div>
  `,

  data() {
    return {
      formData: {
        username: '',
        email: '',
        password: '',
        image: null
      }
    };
  },

  methods: {
    clearImage() {
      this.formData.image = null;
      this.$refs.fileInput.value = '';
    },
    handleFileUpload(event) {
      this.formData.image = event.target.files[0];
    },
    async handleSubmit() {
      const formData = new FormData();
      formData.append("username", this.formData.username);
      formData.append("email", this.formData.email);
      formData.append("password", this.formData.password);
      if (this.formData.image) {
        formData.append("image", this.formData.image);
      }

      const res = await fetch(location.origin + '/api/user', {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        alert("Registration successful! You can log in now.");
        this.$router.push('/user/login');
      } else if (res.status == 919) {
        alert("Invalid File Type; Allowed Types = ['.jpg', '.jpeg', '.png']");
        this.clearImage();
      } else if (res.status == 400) {
        alert("A user with this email already exists.");
        this.formData.email = '';
      } else if (res.status == 920) {
        alert("A user with this username already exists.");
        this.formData.username = '';
      } else {
        alert("Registration failed.");
      }
    },
  },
};

export default RegistrationPage;
