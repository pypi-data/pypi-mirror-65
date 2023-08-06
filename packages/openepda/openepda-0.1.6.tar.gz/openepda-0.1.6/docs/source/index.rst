.. openepda documentation master file, created by
   sphinx-quickstart on Sun Nov  4 02:02:22 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================
openEPDA Overview
=================

About openEPDA
==============

openEPDA™ is a collection of open standards to be used in electronic-photonic
design automation. These include definition of data interchange formats to
facilitate Foundry PDK distribution and
easier simulation and measurement data exchange between the parties involved
in the PIC design chain. See Section Roadmap for the planned activities.

Roadmap
=======

.. _roadmap:

The following standards / libraries are planned to be included in openEPDA:

* openEPDA data format
* openEPDA data format writer / reader for python
* openEPDA Chip Description File format
* openEPDA Measurement Description File format
* openEPDA equipment API for python
* openEPDA building blocks description format (uPDK)

Authors
=======

.. _authors:

openEPDA is a trademark of TU/e and PITC. openEPDA is maintained by TU/e and
PITC. The full list of contributors is listed on the :ref:`about` page.
Authors and copyright for specific standards are provided on the
corresponding pages.

.. toctree::
   :hidden:
   :caption: Overview

   about
   licensing_policy
   contributing

.. toctree::
   :caption: Standards
   :maxdepth: 2

   openepda_data_format
   openepda_cdf_format
   openepda_mdf_format
   pdk_components
   analytic_expressions

.. toctree::
   :hidden:
   :caption: Python package
   :maxdepth: 2

   pypi_package/api
   pypi_package/history_of_changes

.. toctree::
   :hidden:
   :caption: Other resources

   openEPDA Validation <https://validate.openepda.org>