import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue';
import RegisterPage from '@/views/RegisterPage.vue';
import EmailConfirmationPage from '@/views/EmailConfirmationPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import ProfileOnboarding from '@/views/ProfileOnboarding.vue';
import HomePage from '@/views/Protected/HomePage.vue';
import ExplorePage from '@/views/Protected/ExplorePage.vue';
import MessagesPage from '@/views/Protected/MessagesPage.vue';
import NotificationsPage from '@/views/Protected/NotificationsPage.vue';
import ProfilePage from '@/views/Protected/ProfilePage.vue';
import Vue from '@/views/Protected//profile/View.vue';
import ViewSettings from '@/views/Protected//profile/ViewSettings.vue';
import ViewSettingsMore from '@/views/Protected//profile/ViewSettingsMore.vue';
import ViewSettingsDefault from '@/views/Protected//profile/ViewSettingsDefault.vue';
import ViewSettingsPassword from '@/views/Protected//profile/ViewSettingsPassword.vue';
import Conversation from '@/views/Protected//chat/Conversation.vue';

import OauthPage from '@/views/OauthPage.vue';


import useUserStore from '@/stores/user';
import { useSocketStore } from '@/stores/socket';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomePage,
      meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true },
      children: [
        {
          path: '',
          name: 'home',
          component: ExplorePage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Explore' },
        },
        {
          path: 'messages',
          component: MessagesPage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Chat' },
          children: [
            {
                path: ':id',
                component: Conversation,
                meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Chat' }
            },
          ]
        },
        {
          path: 'notifications',
          component: NotificationsPage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Notifications' }
        },
        {
          path: 'profile/:id',
          component: ProfilePage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile' },
          children: [
            {
              path: '',
              component: Vue,
              meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile' },
            },
            {
              path: 'settings',
              component: ViewSettings,
              meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'Personal details' },
              children : [
                {
                  path: '',
                  component: ViewSettingsDefault,
                  meta: { requiresSameUser: true, requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'Personal details' }
                },
                {
                  path: 'password',
                  component: ViewSettingsPassword,
                  meta: { requiresSameUser: true, requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'Change password' }
                },
                {
                  path: 'details',
                  component: ViewSettingsMore,
                  meta: { requiresSameUser: true, requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'More details' }
                }
              ]
            }

          ]
        },
      ]
    },
    {
      path: '/landing',
      name: 'landing',
      component: LandingPage,
      meta: { public: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
      meta: { public: true }
    },
    {
      path: '/confirm-email', // TODO: I should find a solution to integrate this later
      name: 'email confirmation',
      component: EmailConfirmationPage,
      meta: { requiresVerification: false, requiresAuth: true, requiresCompleteProfile: false }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: { public: true }
    },
    {
      path: '/auth-success',
      name: 'oauth',
      component: OauthPage,
      meta: { public: true }
    },
    {
      path: '/profile-onboarding',
      name: 'profile onboarding',
      component: ProfileOnboarding,
      meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: false }
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const user = useUserStore();
  const socketStore = useSocketStore();
  const token = localStorage.getItem('auth_token');

    if (token && !user.isLoaded) {
      await user.fetchUser();
    }
    if (!token) {
      await user.fetchUser();
      user.setIsLoaded(false)
    }

    if (user.isAuthenticated) {
      if (!user.isVerified && to.meta.requiresVerification) {
        return next({ name: 'email confirmation' });
      } else if (!user.isProfileComplete && to.meta.requiresCompleteProfile) {
        return next({ name: 'profile onboarding' });
      } else {
        if (to.meta.public) {
          return next({ name: 'home' });
        } else if (user.isVerified && !to.meta.requiresVerification) {
          return next({ name: 'profile onboarding' });
        } else if (user.isProfileComplete && !to.meta.requiresCompleteProfile) {
          return next({ name: 'home' });
        }
        if (to.meta.requiresSameUser && to.params.id != user.getUserID) {
          return next({ name: 'home' });
        }
      }
      if (user.isVerified && user.isProfileComplete) socketStore.connectAll()
    } else {
      if (!to.meta.public) {
          return next({ name: 'login' });
      }
    }
    next();
});
export default router
