function googleTranslateElementInit() {
  new google.translate.TranslateElement({
    pageLanguage: 'en',       
    includedLanguages: 'fi',  
    layout: google.translate.TranslateElement.InlineLayout.SIMPLE
  }, 'google_translate_element');
}
