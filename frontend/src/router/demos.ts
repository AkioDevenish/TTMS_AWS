import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import BodyView from '@/layout/BodyView.vue';
import indexHome from '@/pages/dashbords/indexHome.vue';
import indexProject from '@/pages/dashbords/indexProject.vue';
import indexEcommerce from '@/pages/dashbords/indexEcommerce.vue';
import indexGeneral from '@/pages/widgets/indexGeneral.vue';
import indexChart from '@/pages/widgets/indexChart.vue';
import indexFileManeger from '@/pages/demo/filemaneger/indexFileManeger.vue';
import indexKanbanBoard from '@/pages/demo/kanban/indexKanbanBoard.vue';
import indexAddProduct from '@/pages/demo/ecommerce/indexAddProduct.vue';
import indexProduct from '@/pages/demo/ecommerce/indexProduct.vue';
import indexCart from '@/pages/demo/ecommerce/indexCart.vue';
import indexProductPage from '@/pages/demo/ecommerce/indexProductPage.vue';
import indexCheckout from '@/pages/demo/ecommerce/indexCheckout.vue';
import indexPaymentDetail from '@/pages/demo/ecommerce/indexPaymentDetail.vue';
import indexOrder from '@/pages/demo/ecommerce/indexOrder.vue';
import indexWishlist from '@/pages/demo/ecommerce/indexWishlist.vue';
import indexPricing from '@/pages/demo/ecommerce/indexPricing.vue';
import indexInvoiceOne from '@/pages/demo/ecommerce/indexInvoiceOne.vue';
import indexProductList from '@/pages/demo/ecommerce/indexProductList.vue';
import indexInvoiceTwo from '@/pages/demo/ecommerce/indexInvoiceTwo.vue';
import indexInvoiceThree from '@/pages/demo/ecommerce/indexInvoiceThree.vue';
import indexInvoiceFour from '@/pages/demo/ecommerce/indexInvoiceFour.vue';
import indexInvoiceFive from '@/pages/demo/ecommerce/indexInvoiceFive.vue';
import indexInvoiceSix from '@/pages/demo/ecommerce/indexInvoiceSix.vue';
import indexLetterBox from '@/pages/demo/letterbox/indexLetterBox.vue';
import indexPrivateChat from '@/pages/chat/indexPrivateChat.vue';
import indexGroupChat from '@/pages/chat/indexGroupChat.vue';
import indexBookmark from '@/pages/demo/bookmark/indexBookmark.vue';
import indexContact from '@/pages/contacts/indexContact.vue';
import indexTask from '@/pages/task/indexTask.vue';
import indexCalendar from '@/pages/calendar/indexCalendar.vue';
import indexSoical from '@/pages/socialapp/indexSoical.vue';
import indexTodo from '@/pages/todo/indexTodo.vue';
import indexSearch from '@/pages/search/indexSearch.vue';
import indexValidation from '@/pages/demo/forms/formcontrols/indexValidation.vue';
import indexInputs from '@/pages/demo/forms/formcontrols/indexInputs.vue';
import indexCheckbox from '@/pages/demo/forms/formcontrols/indexCheckbox.vue';
import indexGroups from '@/pages/demo/forms/formcontrols/indexGroups.vue';
import indexMask from '@/pages/demo/forms/formcontrols/indexMask.vue';
import indexMega from '@/pages/demo/forms/formcontrols/indexMega.vue';
import indexDatapicker from '@/pages/demo/forms/formwidgets/indexDatapicker.vue';
import indexTouchspin from '@/pages/demo/forms/formwidgets/indexTouchspin.vue';
import indexSelect from '@/pages/demo/forms/formwidgets/indexSelect.vue';
import indexTypeahead from '@/pages/demo/forms/formwidgets/indexTypeahead.vue';
import indexClipboard from '@/pages/demo/forms/formwidgets/indexClipboard.vue';
import indexSwitch from '@/pages/demo/forms/formwidgets/indexSwitch.vue';
import formWizard from '@/pages/demo/forms/formlayout/formWizard.vue';
import formWizard2 from '@/pages/demo/forms/formlayout/formWizard2.vue';
import indexTwofactor from '@/pages/demo/forms/formlayout/indexTwofactor.vue';
import indexBootstrap from '@/pages/table/indexBootstrap.vue';
import indexComponent from '@/pages/table/indexComponent.vue';
import indexInit from '@/pages/table/indexInit.vue';
import indexTypography from '@/pages/uikits/indexTypography.vue';
import indexAvatars from '@/pages/uikits/indexAvatars.vue';
import indexHelper from '@/pages/uikits/indexHelper.vue';
import indexGrid from '@/pages/uikits/indexGrid.vue';
import indexTagPills from '@/pages/uikits/indexTagPills.vue';
import indexProgress from '@/pages/uikits/indexProgress.vue';
import indexModal from '@/pages/uikits/indexModal.vue';
import indexAlert from '@/pages/uikits/indexAlert.vue';
import indexPopover from '@/pages/uikits/indexPopover.vue';
import indexTooltip from '@/pages/uikits/indexTooltip.vue';
import indexDropdown from '@/pages/uikits/indexDropdown.vue';
import indexAccordion from '@/pages/uikits/indexAccordion.vue';
import indexTabs from '@/pages/uikits/indexTabs.vue';
import indexLists from '@/pages/uikits/indexLists.vue';
import indexAnimate from '@/pages/demo/animation/indexAnimate.vue';
import indexAos from '@/pages/demo/animation/indexAos.vue';
import indexFlag from '@/pages/demo/icons/indexFlag.vue';
import indexFontawesome from '@/pages/demo/icons/indexFontawesome.vue';
import indexThemify from '@/pages/demo/icons/indexThemify.vue';
import indexIcoicon from '@/pages/demo/icons/indexIcoicon.vue';
import indexFeather from '@/pages/demo/icons/indexFeather.vue';
import indexWhether from '@/pages/demo/icons/indexWhether.vue';
import indexDefaultStyle from '@/pages/buttons/indexDefaultStyle.vue';
import indexFlat from '@/pages/buttons/indexFlat.vue';
import indexEdge from '@/pages/buttons/indexEdge.vue';
import indexRaised from '@/pages/buttons/indexRaised.vue';
import indexGroup from '@/pages/buttons/indexGroup.vue';
import indexApexchart from '@/pages/charts/indexApexchart.vue';
import indexGoogle from '@/pages/charts/indexGoogle.vue';
import indexChartist from '@/pages/charts/indexChartist.vue';
import indexSample from '@/pages/samplepage/indexSample.vue';
import indexInternationalization from '@/pages/internationalization/indexInternationalization.vue';
import indexErrorPage1 from '@/pages/demo/error/indexErrorPage1.vue';
import indexErrorPage2 from '@/pages/demo/error/indexErrorPage2.vue';
import indexErrorPage3 from '@/pages/demo/error/indexErrorPage3.vue';
import indexErrorPage4 from '@/pages/demo/error/indexErrorPage4.vue';
import indexErrorPage5 from '@/pages/demo/error/indexErrorPage5.vue';
import indexErrorPage6 from '@/pages/demo/error/indexErrorPage6.vue';
import indexComingsoonPage from '@/pages/comingsoon/indexComingsoonPage.vue';
import indexComingsoonImage from '@/pages/comingsoon/indexComingsoonImage.vue';
import indexComingsoonVideo from '@/pages/comingsoon/indexComingsoonVideo.vue';
import loginSimple from '@/pages/authentication/loginSimple.vue';
import loginImage from '@/pages/authentication/loginImage.vue';
import loginImageTwo from '@/pages/authentication/loginImageTwo.vue';
import loginValidation from '@/pages/authentication/loginValidation.vue';
import loginTooltip from '@/pages/authentication/loginTooltip.vue';
import loginSweetalert from '@/pages/authentication/loginSweetalert.vue';
import registerSimple from '@/pages/authentication/registerSimple.vue';
import registerImage from '@/pages/authentication/registerImage.vue';
import registerImageTwo from '@/pages/authentication/registerImageTwo.vue';
import unlockUser from '@/pages/authentication/unlockUser.vue';
import forgetPassword from '@/pages/authentication/forgetPassword.vue';
import resetPassword from '@/pages/authentication/resetPassword.vue';
import maintenanceView from '@/pages/authentication/maintenanceView.vue';
import indexGallery from '@/pages/demo/gallery/indexGallery.vue';
import indexGriddesc from '@/pages/demo/gallery/indexGriddesc.vue';
import indexMasonry from '@/pages/demo/gallery/indexMasonry.vue';
import indexMasonarydesc from '@/pages/demo/gallery/indexMasonarydesc.vue';
import indexHoverGallery from '@/pages/demo/gallery/indexHoverGallery.vue';
import indexDetails from '@/pages/demo/blog/indexDetails.vue';
import indexSingle from '@/pages/demo/blog/indexSingle.vue';
import indexAdd from '@/pages/demo/blog/indexAdd.vue';
import indexFaq from '@/pages/faq/indexFaq.vue';
import indexJobCard from '@/pages/demo/job/indexCard.vue';
import indexList from '@/pages/demo/job/indexList.vue';
import indexJobDetails from '@/pages/demo/job/indexDetails.vue';
import indexApply from '@/pages/demo/job/indexApply.vue';
import indexLearning from '@/pages/demo/learning/indexLearning.vue';
import indexGoogleMap from '@/pages/demo/maps/indexGoogle.vue';
import indexCourse from '@/pages/demo/learning/indexCourse.vue';
import indexLeaflet from '@/pages/demo/maps/indexLeaflet.vue';
import indexCk from '@/pages/demo/editor/indexCk.vue';
import simpleEditor from '@/pages/demo/editor/simpleEditor.vue';
import indexKnowledgebase from '@/pages/faq/indexFaq.vue';
import indexScrollable from '@/pages/demo/advance/indexScrollable.vue';
import indexTree from '@/pages/demo/advance/indexTree.vue';
import indexToasts from '@/pages/demo/advance/indexToasts.vue';
import indexRating from '@/pages/demo/advance/indexRating.vue';
import indexDropzone from '@/pages/demo/advance/indexDropzone.vue';
import indexTour from '@/pages/demo/advance/indexTour.vue';
import indexSweetalert from '@/pages/demo/advance/indexSweetalert.vue';
import animationModal from '@/pages/demo/advance/animationModal.vue';
import owlCarousel from '@/pages/demo/advance/owlCarousel.vue';
import indexCropper from '@/pages/demo/advance/indexCropper.vue';
import indexBasiccard from '@/pages/demo/advance/indexBasiccard.vue';
import indexCreative from '@/pages/demo/advance/indexCreative.vue';
import indexDraggable from '@/pages/demo/advance/indexDraggable.vue';
import indexTimeline from '@/pages/demo/advance/indexTimeline.vue';
import indexRibbon from '@/pages/demo/advance/indexRibbon.vue';
import indexPagenation from '@/pages/demo/advance/indexPagenation.vue';
import indexBreadcrumb from '@/pages/demo/advance/indexBreadcrumb.vue';
import indexRange from '@/pages/demo/advance/indexRange.vue';

const demoRoutes: Array<RouteRecordRaw> = [
  {
    path: '/dashboards',
    component: BodyView,
    children: [
      {
        path: 'Main_Dashboard',
        name: 'Main',
        component: indexHome,
        meta: {
          title: 'Dashboards | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'dashboard_project',
        name: 'project',
        component: indexProject,
        meta: {
          title: 'Dashboards CRM | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'dashboard_ecommerce',
        name: 'ecommerce',
        component: indexEcommerce,
        meta: {
          title: 'Dashboards Ecommerce | MDPS',
          requiresAuth: true
        }
      }
    ]
  },

  {
    path: '/widgets',
    component: BodyView,
    children: [
      {
        path: 'general',
        name: 'General',
        component: indexGeneral,
        meta: {
          title: 'Widgets General | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'Chart',
        name: 'charts',
        component: indexChart,
        meta: {
          title: 'Widgets Chart | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  // {
  //   path: '/',
  //   component: BodyView,
  //   children: [
  //     {
  //       path: 'project_list',
  //       name: 'projectList',
  //       component: indexProjectlist,
  //       meta: {
  //         title: 'Project List | MDPS',
  //         requiresAuth: true
  //       }
  //     },
  //
  //   ]
  // },
  {
    path: '/app',
    component: BodyView,
    children: [
      {
        path: 'file_manager',
        name: 'fileManager',
        component: indexFileManeger,
        meta: {
          title: 'File Manager | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'kanban_board',
        name: 'kanbanBoard',
        component: indexKanbanBoard,
        meta: {
          title: 'Kanban Board | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'letter_box',
        name: 'letterbox',
        component: indexLetterBox,
        meta: {
          title: 'Letter Box| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'private_chat',
        name: 'Chatapp',
        component: indexPrivateChat,
        meta: {
          title: 'Private Chat| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'group_chat',
        name: 'Group Chat',
        component: indexGroupChat,
        meta: {
          title: 'Group Chat| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'bookmark',
        name: 'bookmark',
        component: indexBookmark,
        meta: {
          title: 'Bookmark| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'contact',
        name: 'contacts',
        component: indexContact,
        meta: {
          title: 'contact| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'todo',
        name: 'todo',
        component: indexTodo,
        meta: {
          title: 'To Do| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'task',
        name: 'task',
        component: indexTask,
        meta: {
          title: 'Task| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'calendar',
        name: 'calendar',
        component: indexCalendar,
        meta: {
          title: 'Calendar| MDPS',
          requiresAuth: true
        }
      }

    ]
  },
  {
    path: '/ecommerce',
    component: BodyView,
    children: [
      {
        path: 'add_product',
        name: 'addporduct',
        component: indexAddProduct,
        meta: {
          title: 'Add Product | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'product',
        name: 'product',
        component: indexProduct,
        meta: {
          title: 'Product | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'cart',
        name: 'cart',
        component: indexCart,
        meta: {
          title: 'Cart | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'details/:id',
        name: 'productPage',
        component: indexProductPage,
        meta: {
          title: 'Product Page | MDPS',
          requiresAuth: true
        }
      },

      {
        path: 'payment_details',
        name: 'paymentDetail',
        component: indexPaymentDetail,
        meta: {
          title: 'Payment Detail | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'invoice_1',
        name: 'Invoice_1',
        component: indexInvoiceOne,
        meta: {
          title: 'Invoice | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'invoice_2',
        name: 'Invoice_2',
        component: indexInvoiceTwo,
        meta: {
          title: 'Invoice Two | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'invoice_3',
        name: 'Invoice_3',
        component: indexInvoiceThree,
        meta: {
          title: 'Invoice Three | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'invoice_4',
        name: 'Invoice_4',
        component: indexInvoiceFour,
        meta: {
          title: 'Invoice Four | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'invoice_5',
        name: 'Invoice_5',
        component: indexInvoiceFive,
        meta: {
          title: 'Invoice Five | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'invoice_6',
        name: 'Invoice_6',
        component: indexInvoiceSix,
        meta: {
          title: 'Invoice Six | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'checkout',
        name: 'Checkout',
        component: indexCheckout,
        meta: {
          title: 'Checkout | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'pricing',
        name: 'pricing',
        component: indexPricing,
        meta: {
          title: 'Pricing | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'wishlist',
        name: 'Wishlist',
        component: indexWishlist,
        meta: {
          title: 'Wish List | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'order_history',
        name: 'Orderhistory',
        component: indexOrder,
        meta: {
          title: 'Order History | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'product_list',
        name: 'productlist',
        component: indexProductList,
        meta: {
          title: 'Product list | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/pages',
    component: BodyView,
    children: [
      {
        path: 'social_app',
        name: 'socialapp',
        component: indexSoical,
        meta: {
          title: 'Social App| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'search',
        name: 'searchresult',
        component: indexSearch,
        meta: {
          title: 'Search| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'sample_page',
        name: 'samplepage',
        component: indexSample,
        meta: {
          title: 'Simple Page| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'internationalization',
        name: 'Internationalization',
        component: indexInternationalization,
        meta: {
          title: 'Internationalization| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'faq',
        name: 'faq',
        component: indexFaq,
        meta: {
          title: 'Faq| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'knowledgebase',
        name: 'knowledgebase',
        component: indexKnowledgebase,
        meta: {
          title: 'Knowledge Base | Documentation',
          requiresAuth: true
        }
      }
    ]
  },

  {
    path: '/form',
    component: BodyView,
    children: [
      {
        path: 'validation',
        name: 'formValidation',
        component: indexValidation,
        meta: {
          title: 'Form Controls Form Validation | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'base_inputs',
        name: 'indexInputs',
        component: indexInputs,
        meta: {
          title: 'Form Controls Base Input | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'checkbox_radio',
        name: 'indexCheckbox',
        component: indexCheckbox,
        meta: {
          title: 'Form Controls Checkbox & Radio | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'select2',
        name: 'Select',
        component: indexSelect,
        meta: {
          title: 'Form Widgets Select | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'input_groups',
        name: 'indexGroups',
        component: indexGroups,
        meta: {
          title: 'Form Controls Input Groups | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'input_mask',
        name: 'indexMask',
        component: indexMask,
        meta: {
          title: 'Form Controls Input Mask | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'mega_options',
        name: 'indexMega',
        component: indexMega,
        meta: {
          title: 'Form Controls Mega Options | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'datepicker',
        name: 'datapicker',
        component: indexDatapicker,
        meta: {
          title: 'Form Widgets Datepicker | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'touchspin',
        name: 'indexTouchspin',
        component: indexTouchspin,
        meta: {
          title: 'Form Widgets Touchspin | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'switch',
        name: 'indexSwitch',
        component: indexSwitch,
        meta: {
          title: 'Form Widgets Switch| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'typeahead',
        name: 'indexTypeahead',
        component: indexTypeahead,
        meta: {
          title: 'Form Widgets Typeahead | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'clipboard',
        name: 'indexClipboard',
        component: indexClipboard,
        meta: {
          title: 'Form Widgets Clipboard | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'form_wizard_two',
        name: 'formWizardtwo',
        component: formWizard2,
        meta: {
          title: 'Form Layout Form Wizard 2 | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'two_actor',
        name: 'Two Factor',
        component: indexTwofactor,
        meta: {
          title: 'Form Layout Two Factor| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'form_wizard',
        name: 'formWizard',
        component: formWizard,
        meta: {
          title: 'Form Layout Form Wizard 2| MDPS',
          requiresAuth: true
        }
      },
    ]
  },
  {
    path: '/table',
    component: BodyView,
    children: [
      {
        path: 'basic',
        name: 'bootstrp',
        component: indexBootstrap,
        meta: {
          title: 'Table Bootstrap Table | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'table_components',
        name: 'tablecomponent',
        component: indexComponent,
        meta: {
          title: 'Table Table Components | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'datatable_basic',
        name: 'basicinit',
        component: indexInit,
        meta: {
          title: 'Table Basic Init | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/uikits',
    component: BodyView,
    children: [
      {
        path: 'typography',
        name: 'Typography',
        component: indexTypography,
        meta: {
          title: 'Uikits Typography | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'avatars',
        name: 'Avatars',
        component: indexAvatars,
        meta: {
          title: 'Uikits Avatars | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'helper_classes',
        name: 'Helper',
        component: indexHelper,
        meta: {
          title: 'Uikits Helper Classes | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'grid',
        name: 'Grid',
        component: indexGrid,
        meta: {
          title: 'Uikits Grid | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'tag_pills',
        name: 'TagPills',
        component: indexTagPills,
        meta: {
          title: 'Uikits Tag & Pills | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'progress_bar',
        name: 'Progress',
        component: indexProgress,
        meta: {
          title: 'Uikits Progressbar | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'modal',
        name: 'model',
        component: indexModal,
        meta: {
          title: 'Uikits Modal | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'alert',
        name: 'alert',
        component: indexAlert,
        meta: {
          title: 'Uikits Alert | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'popover',
        name: 'popover',
        component: indexPopover,
        meta: {
          title: 'Uikits popover | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'tooltip',
        name: 'tooltip',
        component: indexTooltip,
        meta: {
          title: 'Uikits Tooltip | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'dropdown',
        name: 'Dropdown',
        component: indexDropdown,
        meta: {
          title: 'Uikits Dropdown | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'accordion',
        name: 'Accordion',
        component: indexAccordion,
        meta: {
          title: 'Uikits Accordion | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'tabs',
        name: 'Tabs',
        component: indexTabs,
        meta: {
          title: 'Uikits Tabs | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'lists',
        name: 'lists',
        component: indexLists,
        meta: {
          title: 'Uikits Lists | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/animation',
    component: BodyView,
    children: [
      {
        path: 'animate',
        name: 'animate',
        component: indexAnimate,
        meta: {
          title: 'Animate | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'aos_animation',
        name: 'aos',
        component: indexAos,
        meta: {
          title: 'Aos Animation | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/icons',
    component: BodyView,
    children: [
      {
        path: 'flag',
        name: 'flag',
        component: indexFlag,
        meta: {
          title: 'Icons Flag | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'fontawesome',
        name: 'Fontawesome',
        component: indexFontawesome,
        meta: {
          title: 'Icons Fontawesome | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'themify',
        name: 'Themify',
        component: indexThemify,
        meta: {
          title: 'Icons Themify | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'feather_icon',
        name: 'Feather',
        component: indexFeather,
        meta: {
          title: 'Icons Feather | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'whether',
        name: 'indexWether',
        component: indexWhether,
        meta: {
          title: 'Icons Whether | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'ico',
        name: 'Icoicon',
        component: indexIcoicon,
        meta: {
          title: 'Icons Icoicon | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/buttons',
    component: BodyView,
    children: [
      {
        path: 'default_button',
        name: 'button',
        component: indexDefaultStyle,
        meta: {
          title: 'Buttons Default | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'flat',
        name: 'Flat',
        component: indexFlat,
        meta: {
          title: 'Buttons Flat | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'edge',
        name: 'Edge',
        component: indexEdge,
        meta: {
          title: 'Buttons Edge | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'raised',
        name: 'Raised',
        component: indexRaised,
        meta: {
          title: 'Buttons Raised | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'group',
        name: 'Group',
        component: indexGroup,
        meta: {
          title: 'Buttons Group | MDPS',
          requiresAuth: true
        }
      },

    ]
  },
  {
    path: '/chart',
    component: BodyView,
    children: [
      {
        path: 'apexChart',
        name: 'Apexchart',
        component: indexApexchart,
        meta: {
          title: 'Chart Apex Chart | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'google',
        name: 'google',
        component: indexGoogle,
        meta: {
          title: 'Chart Google Chart | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'chartist',
        name: 'chartist',
        component: indexChartist,
        meta: {
          title: 'Chart Chartist Chart | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/error_page1',
    name: 'errorPage1',
    component: indexErrorPage1,
    meta: {
      title: 'Error Page1 | MDPS',
      requiresAuth: true
    }
  },
  {
    path: '/error_page2',
    name: 'errorPage2',
    component: indexErrorPage2,
    meta: {
      title: 'Error Page2 | MDPS',
      requiresAuth: true
    }
  },
  {
    path: '/error_page3',
    name: 'errorPage3',
    component: indexErrorPage3,
    meta: {
      title: 'Error Page3 | MDPS',
      requiresAuth: true
    }
  },
  {
    path: '/error_page4',
    name: 'errorPage4',
    component: indexErrorPage4,
    meta: {
      title: 'Error Page4 | MDPS',
      requiresAuth: true
    }
  },
  {
    path: '/error_page5',
    name: 'errorPage5',
    component: indexErrorPage5,
    meta: {
      title: 'Error Page5 | MDPS',
      requiresAuth: true
    }
  },
  {
    path: '/error_page6',
    name: 'errorPage6',
    component: indexErrorPage6,
    meta: {
      title: 'Error Page6 | MDPS',
      requiresAuth: true
    }
  },
  {
    path: '/comingsoon/comingsoon_simple',
    name: 'comingsoonPage',
    component: indexComingsoonPage,
    meta: {
      title: 'Comingsoon Page | MDPS',
      requiresAuth: true
    }
  },
  {
    path: '/comingsoon/comingsoon_video',
    name: 'comingsoonVideo',
    component: indexComingsoonVideo,
    meta: {
      title: 'Comingsoon Video | MDPS',
      requiresAuth: true
    }
  },
  {
    path: '/comingsoon/comingsoon_image',
    name: 'comingsoonImage',
    component: indexComingsoonImage,
    meta: {
      title: 'Comingsoon Image | MDPS',
      requiresAuth: true
    }
  },
  {
    path: '/authentication/simple',
    name: 'loginsimple',
    component: loginSimple,
    meta: {
      title: 'Login Simple | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/login/one',
    name: 'loginimage',
    component: loginImage,
    meta: {
      title: 'Login Image | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/login/two',
    name: 'loginImagetwo',
    component: loginImageTwo,
    meta: {
      title: 'Login Image Two | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/login/validate',
    name: 'loginValidation',
    component: loginValidation,
    meta: {
      title: 'Login Validation | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/login/tooltip',
    name: 'loginTooltip',
    component: loginTooltip,
    meta: {
      title: 'Login Tooltip | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/login/sweetalert',
    name: 'loginSweetalert',
    component: loginSweetalert,
    meta: {
      title: 'Login Sweetalert | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/register/two',
    name: 'registerImagetwo',
    component: registerImageTwo,
    meta: {
      title: 'Register Image Two | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/auth/register',
    name: 'registerSimple',
    component: registerSimple,
    meta: {
      title: 'Register | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/register/one',
    name: 'registerImage',
    component: registerImage,
    meta: {
      title: 'Register Image | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/unlock_user',
    name: 'unlockUser',
    component: unlockUser,
    meta: {
      title: 'Unlock User | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/forget_password',
    name: 'forgetPassword',
    component: forgetPassword,
    meta: {
      title: 'Forget Password | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/reset_password',
    name: 'resetPassword',
    component: resetPassword,
    meta: {
      title: 'Reset Password | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/authentication/maintenance',
    name: 'maintenanceView',
    component: maintenanceView,
    meta: {
      title: 'Maintenance | MDPS',
      requiresAuth: false
    }
  },
  {
    path: '/gallery',
    component: BodyView,
    children: [
      {
        path: 'grid_gallery',
        name: 'Gallerygrid',
        component: indexGallery,
        meta: {
          title: 'Grid Gallery | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'gallery_desc',
        name: 'griddesc',
        component: indexGriddesc,
        meta: {
          title: 'Grid Gallery With Desc | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'gallery_masonary',
        name: 'Masonry',
        component: indexMasonry,
        meta: {
          title: 'Masonry | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'gallery_masonary_desc',
        name: 'Masonarydesc',
        component: indexMasonarydesc,
        meta: {
          title: 'Masonry Desc | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'hover_effect',
        name: 'hovergallery',
        component: indexHoverGallery,
        meta: {
          title: 'Hover Gallery | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/blog',
    component: BodyView,
    children: [
      {
        path: 'details',
        name: 'blogdetails',
        component: indexDetails,
        meta: {
          title: 'Blog Details | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'single',
        name: 'blogsingle',
        component: indexSingle,
        meta: {
          title: 'Blog Single | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'add_post',
        name: 'addpost',
        component: indexAdd,
        meta: {
          title: 'Add Post | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/job',
    component: BodyView,
    children: [
      {
        path: 'card',
        name: 'jobcard',
        component: indexJobCard,
        meta: {
          title: 'Job Card | MDPS',
          requiresAuth: true
        }
      },
      {
        path: '/job/details/:id',
        name: 'jobdetails',
        component: indexJobDetails,
        props: true,
        meta: {
          title: 'Job Details | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'apply/:id',
        name: 'jobapply',
        component: indexApply,
        meta: {
          title: 'Job Apply | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'list',
        name: 'joblist',
        component: indexList,
        meta: {
          title: 'Job List | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/learning',
    component: BodyView,
    children: [
      {
        path: 'list',
        name: 'Learninglist',
        component: indexLearning,
        meta: {
          title: 'Learning List | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'details/:id',
        name: 'coursedetailed',
        component: indexCourse,
        meta: {
          title: 'course Detailed | MDPS',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/maps',
    component: BodyView,
    children: [
      {
        path: 'vue_google_maps',
        name: 'googlemaps',
        component: indexGoogleMap,
        meta: {
          title: 'Google Map | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'vue_leaflet_maps',
        name: 'mapLeaflet',
        component: indexLeaflet,
        meta: {
          title: 'Leaflet Map | MDPS',
          requiresAuth: true
        }
      },

    ]
  },
  {
    path: '/editor',
    component: BodyView,
    children: [
      {
        path: 'simple_editor',
        name: 'simpleEditor',
        component: simpleEditor,
        meta: {
          title: 'Simple Editor | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'ck_editor',
        name: 'ckeditor',
        component: indexCk,
        meta: {
          title: 'Ck Editor | MDPS',
          requiresAuth: true
        }
      }
    ]
  },

  {
    path: '/pages/knowledgebase',
    component: BodyView,
    children: [
      {
        path: 'knowledgebase',
        name: 'Knowledgebase',
        component: indexKnowledgebase,
        meta: {
          title: 'Knowledgebase | MDPS',
          requiresAuth: true
        }
      },
    ]
  },

  {
    path: '/advance',
    component: BodyView,
    children: [
      {
        path: 'scrollable',
        name: 'Scrollable',
        component: indexScrollable,
        meta: {
          title: 'Bonus UI  Scrollable | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'tree',
        name: 'tree',
        component: indexTree,
        meta: {
          title: 'Bonus UI  Tree | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'toasts',
        name: 'Toasts',
        component: indexToasts,
        meta: {
          title: 'Bonus UI  Toasts | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'rating',
        name: 'rating',
        component: indexRating,
        meta: {
          title: 'Bonus UI  Rating | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'dropzone',
        name: 'Dropzone',
        component: indexDropzone,
        meta: {
          title: 'Bonus UI  Dropzone | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'tour',
        name: 'tour',
        component: indexTour,
        meta: {
          title: 'Bonus UI  Tour | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'sweetalert',
        name: 'sweetalert',
        component: indexSweetalert,
        meta: {
          title: 'Bonus UI  SweetAlert | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'animated_modal',
        name: 'animationModal',
        component: animationModal,
        meta: {
          title: 'Bonus UI  Animated Modal | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'owl_carousel',
        name: 'owlCarousel',
        component: owlCarousel,
        meta: {
          title: 'Bonus UI  Owl Carousel | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'ribbons',
        name: 'ribbon',
        component: indexRibbon,
        meta: {
          title: 'Bonus UI  Ribbons | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'pagination',
        name: 'pagenation',
        component: indexPagenation,
        meta: {
          title: 'Bonus UI  Pagenation | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'breadcrumb',
        name: 'Breadcrumb',
        component: indexBreadcrumb,
        meta: {
          title: 'Bonus UI  Breadcrumb | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'range_slider',
        name: 'Range',
        component: indexRange,
        meta: {
          title: 'Bonus UI  Range | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'image_cropper',
        name: 'imageCropper',
        component: indexCropper,
        meta: {
          title: 'Bonus UI  imageCropper | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'basic_card',
        name: 'Basiccard',
        component: indexBasiccard,
        meta: {
          title: 'Bonus UI  Basic Card | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'creative_card',
        name: 'Creative',
        component: indexCreative,
        meta: {
          title: 'Bonus UI  Creative Card | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'draggable_card',
        name: 'Draggable',
        component: indexDraggable,
        meta: {
          title: 'Bonus UI  Draggable Card | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'timeline',
        name: 'indexTimeline',
        component: indexTimeline,
        meta: {
          title: 'Bonus UI  Timeline | MDPS',
          requiresAuth: true
        }
      }
    ]
  }
];


export default demoRoutes;
