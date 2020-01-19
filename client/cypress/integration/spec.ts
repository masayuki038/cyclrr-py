it("loads examples", () => {
  cy.visit("http://localhost:5000");
  cy.contains("cyclrr");
});

it("login", () => {
  cy.visit("http://localhost:5000");
  cy.get("#user_name").type('masayuki');
  cy.get("#password").type('masayuki');
  cy.get('.btn-primary').click();
  cy.get('h1').should('contain', 'Hi masayuki!')
});
