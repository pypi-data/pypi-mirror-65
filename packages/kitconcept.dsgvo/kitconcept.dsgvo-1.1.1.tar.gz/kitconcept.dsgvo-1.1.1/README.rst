.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
kitconcept.dsgvo
==============================================================================

.. image:: https://travis-ci.org/kitconcept/kitconcept.dsgvo.svg?branch=master
    :target: https://travis-ci.org/kitconcept/kitconcept.dsgvo

.. image:: https://img.shields.io/pypi/status/kitconcept.dsgvo.svg
    :target: https://pypi.python.org/pypi/kitconcept.dsgvo/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/v/kitconcept.dsgvo.svg
    :target: https://pypi.python.org/pypi/kitconcept.dsgvo
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/kitconcept.dsgvo.svg
    :target: https://pypi.python.org/pypi/kitconcept.dsgvo
    :alt: License

|

.. image:: https://raw.githubusercontent.com/kitconcept/kitconcept.dsgvo/master/kitconcept.png
   :alt: kitconcept
   :target: https://kitconcept.com/

.. warning:: kitconcept is not a law firm. As such, kitconcept does not provide legal advice. The contents and code in this package do not constitute legal advice nor does contributing to the code or communicating with kitconcept or other contributors about the code create an attorney-client relationship.

The General Data Protection Regulation ("GDPR" or "DSGVO" in German) is a regulation in EU law on data protection and privacy for all individuals within the European Union.

kitconcept.dsgvo implements the technical requirements that are necessary to be compliant with this regulation.

We strongly suggest to consult a Plone solution provider for the technical implications and a laywer for the legal implications of the DSGVO/GDPR.

Don't hesitate to contact us under info@kitconcept.com if you need assistance with implementing the DSGVO/GDPR.

Features
========

- [X] Opt-out banner for storing cookies
- [X] Extensible registration form with user confirmation
- [X] Contact form with information text
- [X] Store username, date, time and IP address of the user on registration
- [ ] Export user data

Registration Form
-----------------

Default text (German)::

    "Ich habe die [Link] Datenschutzerklärung und Widerrufhinweise[/Link] gelesen und akzeptiere diese."

Contact Form
------------

Default text (German)::

    "Ihre Anfrage wird verschlüsselt per https an unseren Server geschickt. Sie erklären sich damit einverstanden, dass wir die Angaben zur Beantwortung Ihrer Anfrage verwenden dürfen. Hier finden Sie unsere [Link]Datenschutzerklärung und Widerrufhinweise[/Link]."


Examples
========

This add-on can be seen in action at the following sites:

- VHS-Ehrenamtsportal.de (https://vhs-ehrenamtsportal.de)
- Zeelandia Website (https://www.zeelandia.de)
- HU Berlin Excellence Initiative (https://www.alles-beginnt-mit-einer-frage.de)
- Talke Career Website (https://karriere.talke.com)


Translations
============

This product has been translated into

- German


Installation
============

Install kitconcept.dsgvo by adding it to your buildout::

    [buildout]

    ...

    eggs =
        kitconcept.dsgvo


and then running ``bin/buildout``


Contribute
==========

- Issue Tracker: https://github.com/kitconcept/kitconcept.dsgvo/issues
- Source Code: https://github.com/kitconcept/kitconcept.dsgvo


Support
=======

If you are having issues, or you need assistance implementing the DSGVO / GDPR for your website, don't hesitate to contact us at info@kitconcept.com.


License
=======

The project is licensed under the GPLv2.
