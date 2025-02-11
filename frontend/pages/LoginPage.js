const LoginPage = {
  template: `
<div class="container mt-4 mb-4">
  <div class="card">
    <div class="card-body">

      <form @submit.prevent="handleSubmit" id="login"> 
        <div class="text-center mb-4">
          <h1><u>Login</u></h1>
          <h4>User Login</h4>
        </div>

        <div class="d-flex justify-content-between align-items-center">
          <div>
            <p>(* : Required)</p>

            <div class="mb-2">
              <h2>Email*</h2>
              <input type="email" v-model="email" placeholder="Type Email" class="form-control" style="width: 500px;" required>
            </div>

            <h2>Password*</h2>
            <input type="password" v-model="password" placeholder="Type Password" class="form-control" style="width: 500px;" required>

            <div class="mt-3">
              <button type="submit" class="btn btn-outline-success mb-3">Login</button>
            </div>
            <div class="mt-3">
              <b> In case you haven't registered as either a Sponsor or an Influencer, you may do so by clicking the appropriate link </b>
              <router-link to="/user/registration" class="btn btn-outline-dark mt-2">Register</router-link>
            </div>
          </div>

          <div class="me-5">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="max-width: 200px; height: auto;" class="align-center">
          </div>
        </div>
      </form>

    </div>
  </div>
</div>
    `,

  data() {
    return {
      email: '',
      password: '',
    };
  },

  methods: {
    async handleSubmit() {
      const formData = {
        email: this.email,
        password: this.password,
      };

      const res = await fetch(location.origin + '/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (res.ok) {
        console.log("Login Successful!");

        const data = await res.json();

        localStorage.setItem('user', JSON.stringify(data));
        console.log("User data stored.");

        this.$store.commit('setUser');
        this.$router.push('/dashboard/user');
      } else {
        alert("Invalid email or password.");
        this.email = '';
        this.password = '';
      }
    }
  }
};

export default LoginPage;
