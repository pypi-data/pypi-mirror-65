# Route53 Patterns for the CDK Route53 Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib))
> are auto-generated from CloudFormation. They are stable and safe to use.
>
> However, all other classes, i.e., higher level constructs, are under active development and subject to non-backward
> compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This library contains commonly used patterns for Route53.

## HTTPS Redirect

This construct allows creating a simple domainA -> domainB redirect using CloudFront and S3. You can specify multiple domains to be redirected.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HttpsRedirect(stack, "Redirect",
    record_names=["foo.example.com"],
    target_domain="bar.example.com",
    zone=HostedZone.from_hosted_zone_attributes(stack, "HostedZone",
        hosted_zone_id="ID",
        zone_name="example.com"
    )
)
```

See the documentation of `@aws-cdk/aws-route53-patterns` for more information.
