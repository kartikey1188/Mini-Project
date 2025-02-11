import LoginPage from "../pages/LoginPage.js";
import RegistrationPage from "../pages/RegistrationPage.js";

import store from './store.js'

const routes = [
    {path : '/', component : LoginPage},
    {path : '/user/registration', component : RegistrationPage, meta : {requiresLogin : true, role : "user"}},
    {path : '/campaign/update/:campaign_id', component : UpdateCampaign, props : true, meta : {requiresLogin : true, role : "sponsor"}},
]

const router = new VueRouter({
    routes
})

// navigation guards
router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresLogin)){
        if (!store.state.logged_In_){
            next({path : '/'})
        } 
        else if (to.meta.role && to.meta.role != store.state.role){
            alert('Role not authorized.')
             next({path : '/'})
        } 
        else {
            next();
        }
    } 
    else {
        next();
    }
})

export default router;